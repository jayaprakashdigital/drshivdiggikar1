<?php
/**
 * AJAX handler for load-more & category filter.
 */

defined( 'ABSPATH' ) || exit;

class RA_Ajax {

	public static function init(): void {
		add_action( 'wp_ajax_ra_load_more',        [ __CLASS__, 'load_more' ] );
		add_action( 'wp_ajax_nopriv_ra_load_more', [ __CLASS__, 'load_more' ] );
	}

	public static function load_more(): void {
		check_ajax_referer( 'ra_load_more', 'nonce' );

		$orderby_raw = isset( $_POST['orderby'] ) ? sanitize_text_field( wp_unslash( $_POST['orderby'] ) ) : 'date';
		$order_raw   = isset( $_POST['order'] )   ? strtoupper( sanitize_text_field( wp_unslash( $_POST['order'] ) ) ) : 'DESC';

		$atts = [
			'posts'     => max( 1, min( 50, isset( $_POST['posts'] ) ? (int) $_POST['posts'] : 6 ) ),
			'columns'   => 3,
			'category'  => isset( $_POST['category'] ) ? sanitize_text_field( wp_unslash( $_POST['category'] ) ) : '',
			'orderby'   => in_array( $orderby_raw, [ 'date', 'title', 'rand', 'menu_order' ], true ) ? $orderby_raw : 'date',
			'order'     => in_array( $order_raw, [ 'ASC', 'DESC' ], true ) ? $order_raw : 'DESC',
			'featured'  => ! empty( $_POST['featured'] ) && '1' === (string) $_POST['featured'],
			'date'      => isset( $_POST['date'] ) ? sanitize_text_field( wp_unslash( $_POST['date'] ) ) : '',
			'load_more' => true,
		];

		$page  = max( 1, isset( $_POST['page'] ) ? (int) $_POST['page'] : 2 );
		$args  = RA_Shortcode::build_query_args( $atts, $page );
		$query = new WP_Query( $args );

		if ( ! $query->have_posts() ) {
			wp_send_json_success( [ 'html' => '', 'has_more' => false ] );
		}

		ob_start();
		$i = 0;
		while ( $query->have_posts() ) {
			$query->the_post();
			RA_Shortcode::render_card( get_the_ID(), $i++ );
		}
		wp_reset_postdata();

		wp_send_json_success( [
			'html'     => ob_get_clean(),
			'has_more' => $page < $query->max_num_pages,
		] );
	}
}
