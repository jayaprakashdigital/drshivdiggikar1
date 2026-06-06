<?php
/**
 * Plugin Name:       Recent Articles
 * Plugin URI:        https://github.com/jayaprakashdigital/drshivdiggikar1
 * Description:       Pixel-perfect recent articles card grid with per-post emoji icons, pastel color blocks, category badges, AJAX load-more & Elementor compatibility. Shortcode: [recent_articles].
 * Version:           2.0.0
 * Requires at least: 6.0
 * Requires PHP:      8.0
 * Author:            Dr. Shiv Diggikar
 * License:           GPL v2 or later
 * License URI:       https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain:       recent-articles
 * Domain Path:       /languages
 */

defined( 'ABSPATH' ) || exit;

define( 'RA_VERSION',     '2.0.0' );
define( 'RA_PLUGIN_FILE', __FILE__ );
define( 'RA_PLUGIN_DIR',  plugin_dir_path( __FILE__ ) );
define( 'RA_PLUGIN_URL',  plugin_dir_url( __FILE__ ) );
define( 'RA_TEXT_DOMAIN', 'recent-articles' );

require_once RA_PLUGIN_DIR . 'includes/class-meta-box.php';
require_once RA_PLUGIN_DIR . 'includes/class-shortcode.php';
require_once RA_PLUGIN_DIR . 'includes/class-assets.php';
require_once RA_PLUGIN_DIR . 'includes/class-ajax.php';

add_action( 'plugins_loaded', [ 'RA_Meta_Box', 'init' ] );
add_action( 'plugins_loaded', [ 'RA_Shortcode', 'init' ] );
add_action( 'plugins_loaded', [ 'RA_Assets',    'init' ] );
add_action( 'plugins_loaded', [ 'RA_Ajax',      'init' ] );

register_activation_hook( __FILE__, static function (): void {
	if ( version_compare( PHP_VERSION, '8.0', '<' ) ) {
		deactivate_plugins( plugin_basename( __FILE__ ) );
		wp_die( esc_html__( 'Recent Articles requires PHP 8.0 or higher.', 'recent-articles' ) );
	}
} );
