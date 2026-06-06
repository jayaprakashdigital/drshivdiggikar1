<?php
/**
 * The template for displaying all single posts.
 *
 * Custom design that matches the Dr. Diggikar blog article layout while
 * preserving Astra hooks, sidebar/widget system, SEO/schema/breadcrumb
 * plugins, featured images, and comments.
 *
 * @package Astra Child
 * @since 1.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header(); ?>

<?php while ( have_posts() ) : the_post(); ?>

	<?php
	// Featured image (optional).
	$dsd_thumb = has_post_thumbnail() ? get_the_post_thumbnail_url( get_the_ID(), 'full' ) : '';

	// Primary category for the badge.
	$dsd_cats     = get_the_category();
	$dsd_category = ! empty( $dsd_cats ) ? $dsd_cats[0] : null;
	?>

	<section class="dsd-article-hero<?php echo $dsd_thumb ? ' has-thumb' : ''; ?>"
		<?php if ( $dsd_thumb ) : ?>style="--dsd-hero-bg:url('<?php echo esc_url( $dsd_thumb ); ?>');"<?php endif; ?>>
		<div class="dsd-container">
			<div class="dsd-hero-inner">
				<?php astra_child_breadcrumb(); ?>

				<?php if ( $dsd_category ) : ?>
					<a class="dsd-category-badge" href="<?php echo esc_url( get_category_link( $dsd_category->term_id ) ); ?>">
						<span aria-hidden="true">🏥</span>
						<?php echo esc_html( $dsd_category->name ); ?>
					</a>
				<?php endif; ?>

				<h1 class="dsd-article-title"><?php the_title(); ?></h1>

				<div class="dsd-article-meta">
					<span class="dsd-meta-item">
						<span aria-hidden="true">👨‍⚕️</span> <?php the_author(); ?>
					</span>
					<span class="dsd-meta-dot"></span>
					<span class="dsd-meta-item">
						<span aria-hidden="true">📅</span>
						<time datetime="<?php echo esc_attr( get_the_date( DATE_W3C ) ); ?>"><?php echo esc_html( get_the_date() ); ?></time>
					</span>
					<span class="dsd-meta-dot"></span>
					<span class="dsd-meta-item">
						<span aria-hidden="true">⏱</span>
						<?php
						/* translators: %d: reading time in minutes. */
						printf( esc_html__( '%d min read', 'astra-child' ), (int) astra_child_reading_time() );
						?>
					</span>
				</div>
			</div>
		</div>
	</section>

	<?php astra_primary_content_top(); ?>

	<div class="dsd-container dsd-content-wrap-outer">
		<div class="dsd-content-wrap">

			<?php if ( astra_page_layout() === 'left-sidebar' ) : ?>
				<aside class="dsd-sidebar dsd-sidebar-left"><?php get_sidebar(); ?></aside>
			<?php endif; ?>

			<div id="primary" <?php astra_primary_class(); ?>>
				<article id="post-<?php the_ID(); ?>" <?php post_class( 'dsd-article-body' ); ?>>

					<?php if ( has_post_thumbnail() && ! is_singular( 'attachment' ) ) : ?>
						<figure class="dsd-featured-image">
							<?php the_post_thumbnail( 'large', array( 'loading' => 'eager' ) ); ?>
						</figure>
					<?php endif; ?>

					<div class="dsd-entry-content">
						<?php
						the_content();

						wp_link_pages(
							array(
								'before' => '<div class="dsd-page-links">' . esc_html__( 'Pages:', 'astra-child' ),
								'after'  => '</div>',
							)
						);
						?>
					</div>

					<?php if ( get_the_tags() ) : ?>
						<div class="dsd-post-tags">
							<?php the_tags( '<span class="dsd-tags-label">' . esc_html__( 'Tags:', 'astra-child' ) . '</span> ', ' ', '' ); ?>
						</div>
					<?php endif; ?>

					<?php
					$author_bio = get_the_author_meta( 'description' );
					if ( $author_bio ) :
						?>
						<div class="dsd-author-box">
							<div class="dsd-author-avatar">
								<?php echo get_avatar( get_the_author_meta( 'ID' ), 96, '', '', array( 'class' => 'dsd-author-img' ) ); ?>
							</div>
							<div class="dsd-author-meta">
								<div class="dsd-author-name"><?php the_author(); ?></div>
								<?php
								$credentials = get_the_author_meta( 'credentials' );
								if ( $credentials ) :
									?>
									<div class="dsd-author-creds"><?php echo esc_html( $credentials ); ?></div>
								<?php endif; ?>
								<div class="dsd-author-bio"><?php echo wp_kses_post( wpautop( $author_bio ) ); ?></div>
							</div>
						</div>
					<?php endif; ?>

					<?php
					if ( comments_open() || get_comments_number() ) {
						comments_template();
					}
					?>
				</article>
			</div><!-- #primary -->

			<?php if ( astra_page_layout() !== 'no-sidebar' && astra_page_layout() !== 'left-sidebar' ) : ?>
				<aside class="dsd-sidebar dsd-sidebar-right"><?php get_sidebar(); ?></aside>
			<?php endif; ?>

		</div>
	</div>

	<?php astra_primary_content_bottom(); ?>

<?php endwhile; ?>

<?php get_footer(); ?>
