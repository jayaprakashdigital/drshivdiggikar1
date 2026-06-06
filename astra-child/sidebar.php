<?php
/**
 * Single-post sidebar — wraps Astra's standard sidebar with a class hook
 * the blog-single stylesheet can target. All widgets remain dynamic.
 *
 * @package Astra Child
 * @since 1.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

$astra_sidebar = apply_filters( 'astra_get_sidebar', 'sidebar-1' );

echo '<div ';
	echo wp_kses_post(
		astra_attr(
			'sidebar',
			array(
				'id'    => 'secondary',
				'class' => join( ' ', array_merge( astra_get_secondary_class(), array( 'dsd-secondary' ) ) ),
			)
		)
	);
	echo '>';
?>

	<div class="sidebar-main dsd-sidebar-main" <?php /** @psalm-suppress TooManyArguments */ echo apply_filters( 'astra_sidebar_data_attrs', '', $astra_sidebar ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped, Generic.Commenting.DocComment.MissingShort ?>>
		<?php astra_sidebars_before(); ?>

		<?php
		if ( is_active_sidebar( $astra_sidebar ) ) {
			dynamic_sidebar( $astra_sidebar );
		}

		astra_sidebars_after();
		?>

	</div><!-- .sidebar-main -->
</div><!-- #secondary -->
