/**
 * Recent Articles — Frontend JS
 * Date filter + AJAX load-more.
 */
( function ( $, cfg ) {
	'use strict';

	if ( ! $ || ! cfg || ! cfg.ajaxUrl ) { return; }

	// Date filter dropdown change → reset to page 1, replace grid.
	$( document ).on( 'change.raDate', '.ra-wrapper .ra-date-select', function () {
		var $sel     = $( this );
		var $wrapper = $sel.closest( '.ra-wrapper' );
		var value    = $sel.val();
		value = ( value === null || value === undefined ) ? '' : String( value );

		$wrapper.attr( 'data-date', value );

		// Reset load-more state (button may be currently hidden — that's fine).
		$wrapper.find( '.ra-load-more-btn' )
			.removeClass( 'is-loading' )
			.prop( 'disabled', false )
			.attr( 'data-page', '2' )
			.find( '.ra-btn-text' ).text( cfg.loadMoreTxt );

		fetchPosts( $wrapper, 1, true );
	} );

	// Load More.
	$( document ).on( 'click.raLoadMore', '.ra-wrapper .ra-load-more-btn', function () {
		var $btn     = $( this );
		var $wrapper = $btn.closest( '.ra-wrapper' );
		if ( $btn.prop( 'disabled' ) ) { return; }

		var page = parseInt( $btn.attr( 'data-page' ), 10 );
		if ( isNaN( page ) || page < 2 ) { page = 2; }
		fetchPosts( $wrapper, page, false );
	} );

	function fetchPosts( $wrapper, page, replace ) {
		var $grid = $wrapper.find( '.ra-grid' );
		var $wrap = $wrapper.find( '.ra-load-more-wrap' );
		var $btn  = $wrap.find( '.ra-load-more-btn' );

		$btn.addClass( 'is-loading' ).prop( 'disabled', true );
		$grid.attr( 'aria-busy', 'true' );

		$.post( cfg.ajaxUrl, {
			action:   'ra_load_more',
			nonce:    $wrapper.attr( 'data-nonce' ) || cfg.nonce,
			posts:    $wrapper.attr( 'data-posts' ) || '6',
			category: $wrapper.attr( 'data-category' ) || '',
			orderby:  $wrapper.attr( 'data-orderby' )  || 'date',
			order:    $wrapper.attr( 'data-order' )   || 'DESC',
			featured: $wrapper.attr( 'data-featured' ) || '0',
			date:     $wrapper.attr( 'data-date' )    || '',
			page:     page
		} )
		.done( function ( res ) {
			if ( ! res || ! res.success || ! res.data ) {
				showButton( $wrap, $btn, false, cfg.errorTxt );
				return;
			}

			var html    = res.data.html    || '';
			var hasMore = !! res.data.has_more;

			if ( replace ) {
				if ( html ) {
					$grid.html( html );
				} else {
					$grid.empty().append(
						'<p class="ra-no-posts">' + escapeHtml( cfg.noPostsTxt ) + '</p>'
					);
				}
			} else if ( html ) {
				var $cards = $( html ).addClass( 'ra-card--dynamic' );
				$grid.append( $cards );
				$cards.first().find( 'a' ).first().trigger( 'focus' );
			}

			if ( hasMore ) {
				showButton( $wrap, $btn, true, cfg.loadMoreTxt );
				$btn.attr( 'data-page', replace ? 2 : page + 1 );
			} else {
				// Hide entirely instead of leaving a disabled stub.
				hideButton( $wrap, $btn );
			}
		} )
		.fail( function () {
			showButton( $wrap, $btn, false, cfg.errorTxt );
		} )
		.always( function () {
			$grid.attr( 'aria-busy', 'false' );
		} );
	}

	function showButton( $wrap, $btn, enabled, label ) {
		$wrap.removeClass( 'is-hidden' );
		$btn.removeClass( 'is-loading' )
			.prop( 'disabled', ! enabled )
			.find( '.ra-btn-text' ).text( label );
	}

	function hideButton( $wrap, $btn ) {
		$btn.removeClass( 'is-loading' ).prop( 'disabled', true );
		$wrap.addClass( 'is-hidden' );
	}

	function escapeHtml( s ) {
		return String( s ).replace( /[&<>"']/g, function ( c ) {
			return { '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' }[ c ];
		} );
	}

} )( window.jQuery, window.raConfig || {} );
