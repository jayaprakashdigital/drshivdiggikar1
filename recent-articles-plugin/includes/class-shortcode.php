<?php
/**
 * [recent_articles] shortcode — renders a responsive card grid.
 *
 * Cards use a colored top block with a centered emoji icon (per-post meta),
 * a category badge whose color comes from per-post meta, title, excerpt, and
 * an author / Read CTA footer.
 */

defined( 'ABSPATH' ) || exit;

class RA_Shortcode {

	/** Fallback palette used when a post has no `_ra_bg_color` meta. */
	private const FALLBACK_BG = [
		'#FCEFD5', '#D5F0E5', '#E5DDF8',
		'#FBD9D8', '#D7F2D7', '#FBE4C7',
	];

	/** Fallback badge accent palette (mapped by index alongside FALLBACK_BG). */
	private const FALLBACK_BADGE = [
		'#B45309', '#0F766E', '#6D28D9',
		'#BE123C', '#15803D', '#C2410C',
	];

	public static function init(): void {
		add_shortcode( 'recent_articles', [ __CLASS__, 'render' ] );
	}

	// ── Attribute parsing ─────────────────────────────────────────────────

	private static function parse_atts( array $atts ): array {
		$defaults = [
			'posts'       => 6,
			'columns'     => 3,
			'category'    => '',
			'show_filter' => 'true',
			'load_more'   => 'true',
			'orderby'     => 'date',
			'order'       => 'DESC',
			'featured'    => 'no',
			'heading'     => '',
			'label'       => '',
		];

		$atts = shortcode_atts( $defaults, $atts, 'recent_articles' );

		return [
			'posts'       => max( 1, min( 50, (int) $atts['posts'] ) ),
			'columns'     => max( 1, min( 4,  (int) $atts['columns'] ) ),
			'category'    => sanitize_text_field( $atts['category'] ),
			'show_filter' => filter_var( $atts['show_filter'], FILTER_VALIDATE_BOOLEAN ),
			'load_more'   => filter_var( $atts['load_more'],   FILTER_VALIDATE_BOOLEAN ),
			'orderby'     => in_array( $atts['orderby'], [ 'date', 'title', 'rand', 'menu_order' ], true )
				? $atts['orderby'] : 'date',
			'order'       => in_array( strtoupper( (string) $atts['order'] ), [ 'ASC', 'DESC' ], true )
				? strtoupper( $atts['order'] ) : 'DESC',
			'featured'    => filter_var( $atts['featured'], FILTER_VALIDATE_BOOLEAN ),
			'heading'     => sanitize_text_field( $atts['heading'] ),
			'label'       => sanitize_text_field( $atts['label'] ),
		];
	}

	// ── WP_Query args builder ─────────────────────────────────────────────

	public static function build_query_args( array $atts, int $page = 1 ): array {
		$args = [
			'post_type'              => 'post',
			'post_status'            => 'publish',
			'posts_per_page'         => $atts['posts'],
			'paged'                  => $page,
			'orderby'                => $atts['orderby'],
			'order'                  => $atts['order'],
			'no_found_rows'          => empty( $atts['load_more'] ),
			'update_post_term_cache' => true,
			'update_post_meta_cache' => true,
			'ignore_sticky_posts'    => true,
		];

		if ( ! empty( $atts['category'] ) ) {
			$slugs = array_filter( array_map( 'sanitize_title', explode( ',', $atts['category'] ) ) );
			if ( $slugs ) {
				$args['category_name'] = implode( ',', $slugs );
			}
		}

		if ( ! empty( $atts['featured'] ) ) {
			$args['meta_query'] = [
				[
					'key'   => '_ra_featured',
					'value' => '1',
				],
			];
		}

		return $args;
	}

	// ── Main shortcode output ─────────────────────────────────────────────

	public static function render( $atts ): string {
		$atts = self::parse_atts( (array) $atts );
		$uid  = 'ra-grid-' . wp_unique_id();

		$heading_text = $atts['heading'] ?: __( 'Recent Articles', 'recent-articles' );
		$label_text   = $atts['label']   ?: __( 'LATEST POSTS', 'recent-articles' );

		ob_start();
		?>
		<div
			id="<?php echo esc_attr( $uid ); ?>"
			class="ra-wrapper ra-cols-<?php echo esc_attr( $atts['columns'] ); ?>"
			data-posts="<?php echo esc_attr( $atts['posts'] ); ?>"
			data-columns="<?php echo esc_attr( $atts['columns'] ); ?>"
			data-category="<?php echo esc_attr( $atts['category'] ); ?>"
			data-orderby="<?php echo esc_attr( $atts['orderby'] ); ?>"
			data-order="<?php echo esc_attr( $atts['order'] ); ?>"
			data-featured="<?php echo esc_attr( $atts['featured'] ? '1' : '0' ); ?>"
			data-nonce="<?php echo esc_attr( wp_create_nonce( 'ra_load_more' ) ); ?>"
			role="region"
			aria-label="<?php echo esc_attr( $heading_text ); ?>"
		>
			<div class="ra-section-header">
				<div class="ra-section-header__left">
					<div class="ra-label"><?php echo esc_html( $label_text ); ?></div>
					<h2 class="ra-heading"><?php echo esc_html( $heading_text ); ?></h2>
				</div>
				<a href="<?php echo esc_url( get_permalink( get_option( 'page_for_posts' ) ) ?: home_url( '/blog/' ) ); ?>"
				   class="ra-view-all"
				   aria-label="<?php esc_attr_e( 'View all articles', 'recent-articles' ); ?>">
					<?php esc_html_e( 'View All', 'recent-articles' ); ?> <span aria-hidden="true">&rarr;</span>
				</a>
			</div>

			<?php if ( $atts['show_filter'] ) : ?>
				<?php self::render_filter_tabs( $atts['category'] ); ?>
			<?php endif; ?>

			<div class="ra-grid" role="list" aria-live="polite" aria-relevant="additions">
				<?php
				$query = new WP_Query( self::build_query_args( $atts ) );
				if ( $query->have_posts() ) {
					$i = 0;
					while ( $query->have_posts() ) {
						$query->the_post();
						self::render_card( get_the_ID(), $i++ );
					}
					wp_reset_postdata();
				} else {
					echo '<p class="ra-no-posts">' . esc_html__( 'No posts found.', 'recent-articles' ) . '</p>';
				}
				?>
			</div>

			<?php if ( $atts['load_more'] && ! empty( $query ) && $query->max_num_pages > 1 ) : ?>
			<div class="ra-load-more-wrap">
				<button
					class="ra-load-more-btn"
					type="button"
					data-page="2"
					aria-label="<?php esc_attr_e( 'Load more articles', 'recent-articles' ); ?>"
				>
					<span class="ra-btn-text"><?php esc_html_e( 'Load More', 'recent-articles' ); ?></span>
					<span class="ra-btn-spinner" aria-hidden="true"></span>
				</button>
			</div>
			<?php endif; ?>
		</div>
		<?php
		return ob_get_clean();
	}

	// ── Category filter tabs ──────────────────────────────────────────────

	private static function render_filter_tabs( string $active_cat ): void {
		$terms = get_categories( [
			'hide_empty' => true,
			'orderby'    => 'name',
			'order'      => 'ASC',
		] );

		if ( empty( $terms ) || is_wp_error( $terms ) ) {
			return;
		}
		?>
		<div class="ra-filter-bar" role="tablist" aria-label="<?php esc_attr_e( 'Filter by category', 'recent-articles' ); ?>">
			<button
				type="button"
				class="ra-filter-btn<?php echo empty( $active_cat ) ? ' is-active' : ''; ?>"
				data-category=""
				role="tab"
				aria-selected="<?php echo empty( $active_cat ) ? 'true' : 'false'; ?>"
			>
				<?php esc_html_e( 'All', 'recent-articles' ); ?>
			</button>
			<?php foreach ( $terms as $term ) : ?>
			<button
				type="button"
				class="ra-filter-btn<?php echo ( sanitize_title( $active_cat ) === $term->slug ) ? ' is-active' : ''; ?>"
				data-category="<?php echo esc_attr( $term->slug ); ?>"
				role="tab"
				aria-selected="<?php echo ( sanitize_title( $active_cat ) === $term->slug ) ? 'true' : 'false'; ?>"
			>
				<?php echo esc_html( $term->name ); ?>
			</button>
			<?php endforeach; ?>
		</div>
		<?php
	}

	// ── Single card ───────────────────────────────────────────────────────

	public static function render_card( int $post_id, int $index = 0 ): void {
		$post = get_post( $post_id );
		if ( ! $post ) {
			return;
		}

		$permalink = get_permalink( $post_id );
		$title     = get_the_title( $post_id );

		// Custom excerpt or auto-trimmed.
		$custom_excerpt = (string) RA_Meta_Box::get( $post_id, 'excerpt' );
		$excerpt        = $custom_excerpt !== ''
			? wp_trim_words( $custom_excerpt, 26, '&hellip;' )
			: wp_trim_words( get_the_excerpt( $post_id ), 20, '&hellip;' );

		$date_iso = get_the_date( 'c', $post_id );

		// Reading time — custom or auto.
		$custom_rt = (int) RA_Meta_Box::get( $post_id, 'read_time', 0 );
		$read_time = $custom_rt > 0 ? $custom_rt : self::estimate_read_time( $post->post_content );

		// Category.
		$cats     = get_the_category( $post_id );
		$cat_name = ! empty( $cats ) ? reset( $cats )->name : '';

		// Card colors & icon (per-post meta with palette fallback).
		$bg_color    = (string) RA_Meta_Box::get( $post_id, 'bg_color', '' );
		$badge_color = (string) RA_Meta_Box::get( $post_id, 'badge_color', '' );
		$icon        = (string) RA_Meta_Box::get( $post_id, 'icon', '' );

		if ( '' === $bg_color ) {
			$bg_color = self::FALLBACK_BG[ $index % count( self::FALLBACK_BG ) ];
		}
		if ( '' === $badge_color ) {
			$badge_color = self::FALLBACK_BADGE[ $index % count( self::FALLBACK_BADGE ) ];
		}

		// Author.
		$author_id     = (int) $post->post_author;
		$custom_author = (string) RA_Meta_Box::get( $post_id, 'author_label', '' );
		$author_name   = $custom_author !== '' ? $custom_author : get_the_author_meta( 'display_name', $author_id );
		$initials      = self::get_initials( $author_name );

		$card_style = sprintf(
			'--ra-card-bg:%1$s;--ra-badge-color:%2$s;--ra-badge-bg:%3$s;',
			esc_attr( $bg_color ),
			esc_attr( $badge_color ),
			esc_attr( self::hex_to_rgba( $badge_color, 0.10 ) )
		);
		?>
		<article
			class="ra-card"
			role="listitem"
			itemscope
			itemtype="https://schema.org/Article"
			style="<?php echo esc_attr( $card_style ); ?>"
		>
			<a href="<?php echo esc_url( $permalink ); ?>" class="ra-card__icon-wrap" tabindex="-1" aria-hidden="true">
				<?php if ( $icon !== '' ) : ?>
					<span class="ra-card__icon"><?php echo esc_html( $icon ); ?></span>
				<?php else : ?>
					<span class="ra-card__icon ra-card__icon--default" aria-hidden="true">📄</span>
				<?php endif; ?>
			</a>

			<div class="ra-card__body">
				<div class="ra-card__meta">
					<?php if ( $cat_name ) : ?>
						<span class="ra-card__cat"><?php echo esc_html( strtoupper( $cat_name ) ); ?></span>
					<?php endif; ?>
					<span class="ra-card__read-time" aria-label="<?php echo esc_attr( sprintf( /* translators: %d = minutes */ __( '%d minute read', 'recent-articles' ), $read_time ) ); ?>">
						<svg class="ra-icon-clock" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
						<?php echo esc_html( sprintf( /* translators: %d = minutes */ __( '%d min', 'recent-articles' ), $read_time ) ); ?>
					</span>
				</div>

				<h3 class="ra-card__title" itemprop="headline">
					<a href="<?php echo esc_url( $permalink ); ?>" itemprop="url"><?php echo esc_html( $title ); ?></a>
				</h3>

				<p class="ra-card__excerpt" itemprop="description"><?php echo wp_kses_post( $excerpt ); ?></p>

				<div class="ra-card__footer">
					<div class="ra-card__author" itemprop="author" itemscope itemtype="https://schema.org/Person">
						<span class="ra-card__avatar" aria-hidden="true">
							<span class="ra-card__avatar-fallback"><?php echo esc_html( $initials ); ?></span>
						</span>
						<span class="ra-card__author-name" itemprop="name"><?php echo esc_html( $author_name ); ?></span>
					</div>

					<a
						href="<?php echo esc_url( $permalink ); ?>"
						class="ra-card__read-more"
						aria-label="<?php echo esc_attr( sprintf( /* translators: %s = post title */ __( 'Read: %s', 'recent-articles' ), $title ) ); ?>"
					>
						<?php esc_html_e( 'Read', 'recent-articles' ); ?> <span aria-hidden="true">&rarr;</span>
					</a>
				</div>
			</div>

			<meta itemprop="datePublished" content="<?php echo esc_attr( $date_iso ); ?>">
		</article>
		<?php
	}

	// ── Helpers ───────────────────────────────────────────────────────────

	private static function estimate_read_time( string $content ): int {
		$words = str_word_count( wp_strip_all_tags( $content ) );
		return max( 1, (int) round( $words / 200 ) );
	}

	private static function get_initials( string $name ): string {
		$parts    = preg_split( '/\s+/', trim( $name ) ) ?: [];
		$initials = '';
		foreach ( array_slice( $parts, 0, 2 ) as $part ) {
			if ( '' !== $part ) {
				$initials .= mb_strtoupper( mb_substr( $part, 0, 1 ) );
			}
		}
		return $initials !== '' ? $initials : 'A';
	}

	private static function hex_to_rgba( string $hex, float $alpha = 1.0 ): string {
		$hex = ltrim( $hex, '#' );
		if ( 3 === strlen( $hex ) ) {
			$hex = $hex[0] . $hex[0] . $hex[1] . $hex[1] . $hex[2] . $hex[2];
		}
		if ( ! preg_match( '/^[0-9a-fA-F]{6}$/', $hex ) ) {
			return 'rgba(180,83,9,' . $alpha . ')';
		}
		$r = hexdec( substr( $hex, 0, 2 ) );
		$g = hexdec( substr( $hex, 2, 2 ) );
		$b = hexdec( substr( $hex, 4, 2 ) );
		return sprintf( 'rgba(%d,%d,%d,%.2f)', $r, $g, $b, max( 0, min( 1, $alpha ) ) );
	}
}
