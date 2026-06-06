<?php
/**
 * Conditional asset enqueuing — only loads CSS/JS on pages that contain the
 * `[recent_articles]` shortcode or render it via an Elementor widget.
 */

defined( 'ABSPATH' ) || exit;

class RA_Assets {

	public static function init(): void {
		add_action( 'wp_enqueue_scripts', [ __CLASS__, 'register' ] );
		add_action( 'wp_enqueue_scripts', [ __CLASS__, 'maybe_enqueue' ], 20 );
	}

	public static function register(): void {
		wp_register_style(
			'ra-frontend',
			RA_PLUGIN_URL . 'assets/css/frontend.css',
			[],
			RA_VERSION
		);

		wp_register_script(
			'ra-frontend',
			RA_PLUGIN_URL . 'assets/js/frontend.js',
			[ 'jquery' ],
			RA_VERSION,
			true
		);

		wp_localize_script( 'ra-frontend', 'raConfig', [
			'ajaxUrl'     => admin_url( 'admin-ajax.php' ),
			'nonce'       => wp_create_nonce( 'ra_load_more' ),
			'loadMoreTxt' => __( 'Load More', 'recent-articles' ),
			'noMoreTxt'   => __( 'No more posts', 'recent-articles' ),
			'errorTxt'    => __( 'Something went wrong. Please try again.', 'recent-articles' ),
			'noPostsTxt'  => __( 'No posts found.', 'recent-articles' ),
		] );
	}

	public static function maybe_enqueue(): void {
		if ( ! self::page_has_shortcode() ) {
			return;
		}
		wp_enqueue_style( 'ra-frontend' );
		wp_enqueue_script( 'ra-frontend' );
	}

	private static function page_has_shortcode(): bool {
		// Always load inside Elementor editor / preview so widgets render.
		if ( isset( $_GET['elementor-preview'] ) ) { // phpcs:ignore WordPress.Security.NonceVerification.Recommended
			return true;
		}
		if ( did_action( 'elementor/loaded' ) && function_exists( 'elementor_pro_load_plugin' ) && is_admin() ) {
			return true;
		}

		global $post;
		if ( ! $post instanceof WP_Post ) {
			return false;
		}

		if ( has_shortcode( $post->post_content, 'recent_articles' ) ) {
			return true;
		}

		// Elementor stores widget data in `_elementor_data` JSON.
		$elementor_data = get_post_meta( $post->ID, '_elementor_data', true );
		if ( is_string( $elementor_data ) && str_contains( $elementor_data, 'recent_articles' ) ) {
			return true;
		}

		return false;
	}
}
