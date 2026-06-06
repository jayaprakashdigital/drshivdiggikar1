<?php
/**
 * Per-post meta box for Recent Articles card customization.
 *
 * Fields:
 *   - Card icon (emoji)
 *   - Card background color
 *   - Category badge color
 *   - Reading time (minutes)
 *   - Custom excerpt
 *   - Custom author label
 *
 * Storage: secure post meta with prefix `_ra_`.
 */

defined( 'ABSPATH' ) || exit;

class RA_Meta_Box {

	private const META_PREFIX  = '_ra_';
	private const NONCE_ACTION = 'ra_save_card_meta';
	private const NONCE_NAME   = 'ra_card_meta_nonce';

	/** Allowed emoji icons (curated for medical / parenting context). */
	public const ALLOWED_ICONS = [
		''   => '— None —',
		'🍼' => 'Bottle',
		'🌿' => 'Leaf',
		'💉' => 'Syringe',
		'🫁' => 'Lungs',
		'🧠' => 'Brain',
		'😴' => 'Sleeping',
		'👶' => 'Baby',
		'🫀' => 'Heart',
		'🩺' => 'Stethoscope',
		'💊' => 'Pill',
		'🦠' => 'Microbe',
		'🌡️' => 'Thermometer',
		'🍎' => 'Apple',
		'❤️' => 'Heart Red',
	];

	/** Curated pastel palette for card background blocks. */
	public const PRESET_BG_COLORS = [
		'#FCEFD5', // peach
		'#D5F0E5', // mint
		'#E5DDF8', // lavender
		'#FBD9D8', // pink
		'#D7F2D7', // green
		'#FBE4C7', // sand
		'#D8E9FB', // sky
		'#F8DFE9', // rose
	];

	/** Curated badge accent colors (text/background pairs derived in CSS). */
	public const PRESET_BADGE_COLORS = [
		'#B45309', // amber
		'#0F766E', // teal
		'#6D28D9', // violet
		'#BE123C', // rose
		'#15803D', // emerald
		'#C2410C', // orange
		'#1D4ED8', // blue
		'#9D174D', // pink-deep
	];

	public static function init(): void {
		add_action( 'add_meta_boxes_post', [ __CLASS__, 'register' ] );
		add_action( 'save_post_post',      [ __CLASS__, 'save' ], 10, 2 );
		add_action( 'admin_enqueue_scripts', [ __CLASS__, 'enqueue_admin_assets' ] );
	}

	public static function enqueue_admin_assets( string $hook ): void {
		if ( ! in_array( $hook, [ 'post.php', 'post-new.php' ], true ) ) {
			return;
		}
		$screen = get_current_screen();
		if ( ! $screen || 'post' !== $screen->post_type ) {
			return;
		}
		wp_enqueue_style( 'wp-color-picker' );
		wp_enqueue_script( 'wp-color-picker' );
		wp_enqueue_style(
			'ra-admin',
			RA_PLUGIN_URL . 'assets/css/admin.css',
			[ 'wp-color-picker' ],
			RA_VERSION
		);
		wp_enqueue_script(
			'ra-admin',
			RA_PLUGIN_URL . 'assets/js/admin.js',
			[ 'jquery', 'wp-color-picker' ],
			RA_VERSION,
			true
		);
	}

	public static function register(): void {
		add_meta_box(
			'ra_card_meta',
			__( 'Recent Articles Card', 'recent-articles' ),
			[ __CLASS__, 'render' ],
			'post',
			'side',
			'default'
		);
	}

	public static function render( WP_Post $post ): void {
		wp_nonce_field( self::NONCE_ACTION, self::NONCE_NAME );

		$icon         = self::get( $post->ID, 'icon' );
		$bg_color     = self::get( $post->ID, 'bg_color', '#FCEFD5' );
		$badge_color  = self::get( $post->ID, 'badge_color', '#B45309' );
		$read_time    = (int) self::get( $post->ID, 'read_time', 0 );
		$excerpt      = self::get( $post->ID, 'excerpt' );
		$author_label = self::get( $post->ID, 'author_label' );
		?>
		<div class="ra-meta">
			<p>
				<label for="ra_icon"><strong><?php esc_html_e( 'Card Icon', 'recent-articles' ); ?></strong></label><br>
				<select name="ra_icon" id="ra_icon" class="widefat">
					<?php foreach ( self::ALLOWED_ICONS as $emoji => $label ) : ?>
						<option value="<?php echo esc_attr( $emoji ); ?>" <?php selected( $icon, $emoji ); ?>>
							<?php echo esc_html( ( $emoji ? $emoji . '  ' : '' ) . $label ); ?>
						</option>
					<?php endforeach; ?>
				</select>
			</p>

			<p>
				<label for="ra_bg_color"><strong><?php esc_html_e( 'Card Background Color', 'recent-articles' ); ?></strong></label><br>
				<input
					type="text"
					name="ra_bg_color"
					id="ra_bg_color"
					class="ra-color-field"
					value="<?php echo esc_attr( $bg_color ); ?>"
					data-default-color="#FCEFD5"
					data-palette="<?php echo esc_attr( wp_json_encode( self::PRESET_BG_COLORS ) ); ?>"
				>
			</p>

			<p>
				<label for="ra_badge_color"><strong><?php esc_html_e( 'Category Badge Color', 'recent-articles' ); ?></strong></label><br>
				<input
					type="text"
					name="ra_badge_color"
					id="ra_badge_color"
					class="ra-color-field"
					value="<?php echo esc_attr( $badge_color ); ?>"
					data-default-color="#B45309"
					data-palette="<?php echo esc_attr( wp_json_encode( self::PRESET_BADGE_COLORS ) ); ?>"
				>
			</p>

			<p>
				<label for="ra_read_time"><strong><?php esc_html_e( 'Reading Time (minutes)', 'recent-articles' ); ?></strong></label><br>
				<input
					type="number"
					min="0"
					max="120"
					name="ra_read_time"
					id="ra_read_time"
					class="small-text"
					value="<?php echo esc_attr( $read_time ); ?>"
				>
				<span class="description"><?php esc_html_e( 'Leave 0 to auto-calculate.', 'recent-articles' ); ?></span>
			</p>

			<p>
				<label for="ra_excerpt"><strong><?php esc_html_e( 'Custom Excerpt', 'recent-articles' ); ?></strong></label><br>
				<textarea
					name="ra_excerpt"
					id="ra_excerpt"
					rows="3"
					class="widefat"
					maxlength="500"
				><?php echo esc_textarea( $excerpt ); ?></textarea>
			</p>

			<p>
				<label for="ra_author_label"><strong><?php esc_html_e( 'Custom Author Label', 'recent-articles' ); ?></strong></label><br>
				<input
					type="text"
					name="ra_author_label"
					id="ra_author_label"
					class="widefat"
					maxlength="100"
					value="<?php echo esc_attr( $author_label ); ?>"
					placeholder="<?php esc_attr_e( 'Defaults to post author', 'recent-articles' ); ?>"
				>
			</p>
		</div>
		<?php
	}

	public static function save( int $post_id, WP_Post $post ): void {
		if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
			return;
		}
		if ( wp_is_post_revision( $post_id ) ) {
			return;
		}
		if ( ! isset( $_POST[ self::NONCE_NAME ] ) ) {
			return;
		}
		if ( ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST[ self::NONCE_NAME ] ) ), self::NONCE_ACTION ) ) {
			return;
		}
		if ( ! current_user_can( 'edit_post', $post_id ) ) {
			return;
		}

		// Icon — only allow values from whitelist.
		$icon_raw = isset( $_POST['ra_icon'] ) ? wp_unslash( $_POST['ra_icon'] ) : '';
		$icon     = is_string( $icon_raw ) && array_key_exists( $icon_raw, self::ALLOWED_ICONS ) ? $icon_raw : '';
		self::set( $post_id, 'icon', $icon );

		// Colors — sanitize as hex.
		$bg    = isset( $_POST['ra_bg_color'] )    ? sanitize_hex_color( wp_unslash( $_POST['ra_bg_color'] ) )    : '';
		$badge = isset( $_POST['ra_badge_color'] ) ? sanitize_hex_color( wp_unslash( $_POST['ra_badge_color'] ) ) : '';
		self::set( $post_id, 'bg_color',    $bg    ?: '' );
		self::set( $post_id, 'badge_color', $badge ?: '' );

		// Reading time — clamp 0-120.
		$rt = isset( $_POST['ra_read_time'] ) ? (int) $_POST['ra_read_time'] : 0;
		$rt = max( 0, min( 120, $rt ) );
		self::set( $post_id, 'read_time', $rt );

		// Excerpt — strip tags, cap length.
		$excerpt = isset( $_POST['ra_excerpt'] ) ? wp_unslash( $_POST['ra_excerpt'] ) : '';
		$excerpt = sanitize_textarea_field( $excerpt );
		$excerpt = mb_substr( $excerpt, 0, 500 );
		self::set( $post_id, 'excerpt', $excerpt );

		// Author label.
		$author_label = isset( $_POST['ra_author_label'] ) ? sanitize_text_field( wp_unslash( $_POST['ra_author_label'] ) ) : '';
		$author_label = mb_substr( $author_label, 0, 100 );
		self::set( $post_id, 'author_label', $author_label );
	}

	public static function get( int $post_id, string $key, $default = '' ) {
		$val = get_post_meta( $post_id, self::META_PREFIX . $key, true );
		return ( '' === $val || null === $val ) ? $default : $val;
	}

	private static function set( int $post_id, string $key, $value ): void {
		if ( '' === $value || null === $value ) {
			delete_post_meta( $post_id, self::META_PREFIX . $key );
		} else {
			update_post_meta( $post_id, self::META_PREFIX . $key, $value );
		}
	}
}
