/**
 * Recent Articles — Frontend JS
 * Category filter + AJAX load-more.
 */
( function ( $, cfg ) {
	'use strict';

	if ( ! cfg || ! cfg.ajaxUrl ) { return; }

	$( document ).on( 'click.raFilter', '.ra-wrapper .ra-filter-btn', function () {
		var $btn     = $( this );
		var $wrapper = $btn.closest( '.ra-wrapper' );
		var category = String( $btn.data( 'category' ) || '' );

		$wrapper.find( '.ra-filter-btn' )
			.removeClass( 'is-active' )
			.attr( 'aria-selected', 'false' );
		$btn.addClass( 'is-active' ).attr( 'aria-selected', 'true' );

		$wrapper.attr( 'data-category', category );
		$wrapper.find( '.ra-load-more-btn' )
			.removeClass( 'is-loading' )
			.prop( 'disabled', false )
			.attr( 'data-page', '2' )
			.show()
			.find( '.ra-btn-text' ).text( cfg.loadMoreTxt );

		fetchPosts( $wrapper, 1, true );
	} );

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
		var $btn  = $wrapper.find( '.ra-load-more-btn' );

		$btn.addClass( 'is-loading' ).prop( 'disabled', true );
		$grid.attr( 'aria-busy', 'true' );

		$.post( cfg.ajaxUrl, {
			action:   'ra_load_more',
			nonce:    $wrapper.attr( 'data-nonce' ) || cfg.nonce,
			posts:    $wrapper.attr( 'data-posts' ),
			category: $wrapper.attr( 'data-category' ) || '',
			orderby:  $wrapper.attr( 'data-orderby' )  || 'date',
			order:    $wrapper.attr( 'data-order' )   || 'DESC',
			featured: $wrapper.attr( 'data-featured' ) || '0',
			page:     page
		} )
		.done( function ( res ) {
			if ( ! res || ! res.success ) {
				setNoMore( $btn, cfg.errorTxt );
				return;
			}
			if ( ! res.data.html ) {
				if ( replace ) { $grid.empty(); }
				setNoMore( $btn, cfg.noMoreTxt );
				return;
			}

			if ( replace ) {
				$grid.html( res.data.html );
			} else {
				var $cards = $( res.data.html ).addClass( 'ra-card--dynamic' );
				$grid.append( $cards );
				$cards.first().find( 'a' ).first().trigger( 'focus' );
			}

			if ( res.data.has_more ) {
				$btn.removeClass( 'is-loading' )
					.prop( 'disabled', false )
					.attr( 'data-page', replace ? 2 : page + 1 )
					.find( '.ra-btn-text' ).text( cfg.loadMoreTxt );
			} else {
				setNoMore( $btn, cfg.noMoreTxt );
			}
		} )
		.fail( function () {
			$btn.removeClass( 'is-loading' )
				.prop( 'disabled', false )
				.find( '.ra-btn-text' ).text( cfg.errorTxt );
		} )
		.always( function () {
			$grid.attr( 'aria-busy', 'false' );
		} );
	}

	function setNoMore( $btn, label ) {
		$btn.removeClass( 'is-loading' )
			.prop( 'disabled', true )
			.find( '.ra-btn-text' ).text( label );
	}

} )( jQuery, window.raConfig || {} );
