/* Recent Articles — initialize color pickers in the post meta box. */
( function ( $ ) {
	'use strict';
	$( function () {
		$( '.ra-color-field' ).each( function () {
			var $field = $( this );
			var raw    = $field.attr( 'data-palette' );
			var palette;
			try { palette = raw ? JSON.parse( raw ) : true; } catch ( e ) { palette = true; }
			$field.wpColorPicker( { palettes: palette } );
		} );
	} );
} )( jQuery );
