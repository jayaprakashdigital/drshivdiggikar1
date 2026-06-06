<?php
/**
 * Astra Child theme functions.
 *
 * @package Astra Child
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Enqueue parent + child styles, plus the dedicated single-post stylesheet.
 */
function astra_child_enqueue_styles() {
	$theme_version = wp_get_theme()->get( 'Version' );

	// Parent Astra stylesheet.
	wp_enqueue_style(
		'astra-parent-style',
		get_template_directory_uri() . '/style.css',
		array(),
		wp_get_theme( 'astra' )->get( 'Version' )
	);

	// Child stylesheet (mainly for theme metadata).
	wp_enqueue_style(
		'astra-child-style',
		get_stylesheet_uri(),
		array( 'astra-parent-style' ),
		$theme_version
	);

	// Single-post stylesheet — only on single posts, for performance.
	if ( is_singular( 'post' ) ) {
		wp_enqueue_style(
			'astra-child-blog-single',
			get_stylesheet_directory_uri() . '/assets/css/blog-single.css',
			array( 'astra-child-style' ),
			$theme_version
		);

		// Poppins web font — preconnect + display=swap for fast paint.
		wp_enqueue_style(
			'astra-child-poppins',
			'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap',
			array(),
			null
		);
	}
}
add_action( 'wp_enqueue_scripts', 'astra_child_enqueue_styles', 15 );

/**
 * Preconnect to Google Fonts for the single-post page.
 */
function astra_child_resource_hints( $urls, $relation_type ) {
	if ( is_singular( 'post' ) && 'preconnect' === $relation_type ) {
		$urls[] = array(
			'href'        => 'https://fonts.googleapis.com',
			'crossorigin',
		);
		$urls[] = array(
			'href'        => 'https://fonts.gstatic.com',
			'crossorigin',
		);
	}
	return $urls;
}
add_filter( 'wp_resource_hints', 'astra_child_resource_hints', 10, 2 );

/**
 * Calculate reading time for the current post (≈ 200 wpm).
 *
 * @param int|WP_Post|null $post Post ID or object. Default: current post.
 * @return int Reading time in minutes (minimum 1).
 */
function astra_child_reading_time( $post = null ) {
	$post = get_post( $post );
	if ( ! $post ) {
		return 1;
	}
	$word_count = str_word_count( wp_strip_all_tags( $post->post_content ) );
	$minutes    = (int) ceil( $word_count / 200 );
	return max( 1, $minutes );
}

/**
 * Render a styled breadcrumb. Uses Yoast / Rank Math / SEOPress if present,
 * otherwise falls back to a simple Home › Blog › Title trail.
 */
function astra_child_breadcrumb() {
	echo '<nav class="dsd-breadcrumb" aria-label="Breadcrumb">';

	if ( function_exists( 'yoast_breadcrumb' ) ) {
		yoast_breadcrumb( '<div class="dsd-breadcrumb-inner">', '</div>' );
	} elseif ( function_exists( 'rank_math_the_breadcrumbs' ) ) {
		rank_math_the_breadcrumbs();
	} elseif ( function_exists( 'seopress_display_breadcrumbs' ) ) {
		seopress_display_breadcrumbs();
	} else {
		$sep   = '<span class="dsd-bc-sep">›</span>';
		$home  = '<a href="' . esc_url( home_url( '/' ) ) . '">' . esc_html__( 'Home', 'astra-child' ) . '</a>';
		$blog_id   = (int) get_option( 'page_for_posts' );
		$blog_link = $blog_id
			? '<a href="' . esc_url( get_permalink( $blog_id ) ) . '">' . esc_html( get_the_title( $blog_id ) ) . '</a>'
			: '<a href="' . esc_url( home_url( '/blog/' ) ) . '">' . esc_html__( 'Blog', 'astra-child' ) . '</a>';
		$title = '<span>' . esc_html( get_the_title() ) . '</span>';
		echo $home . $sep . $blog_link . $sep . $title; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
	}
	echo '</nav>';
}
