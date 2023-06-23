=== Media Library File Size ===
Contributors: SS88_UK
Donate link: https://paypal.me/SS88/
Tags: file size, media library, image size, library size
Requires at least: 4.1
Tested up to: 6.2
Stable tag: 1.3
Requires PHP: 5.6
License: GPL2
License URI: https://www.gnu.org/licenses/gpl-2.0.html

Enhance your Media Library experience with a new column that displays the sizes of files, including collective images, allowing you to conveniently sort them based on file size. Click the 'Index Media' button after installation.

== Description ==

Improve your Media Library functionality by introducing a new column that showcases the sizes of files, including collective images efficiently. This lightweight plugin empowers you to effortlessly sort files based on their respective file sizes. Click the 'Index Media' button after installation.

https://youtu.be/Tt5kdo8NH70

Images and videos play a crucial role in engaging visitors and making a website visually appealing. However, managing these files can become a daunting task, especially when you have a large number of media files on your website. WordPress does offer a media library that allows users to upload and manage media files, but it falls short when it comes to providing information about file sizes. This is where the “Media File Sizes” plugin comes in.

* By default sizes may show without the need to run an index however, indexing the Media Library is highly recommended.
* If sizes do not show, you can click the Index Media button within the Media Library to index/re-index items.
* Shows file size of primary file, plus combined sized for variants (images).
* Ability to order the media items by file size.

== Installation ==

Use the automatic installer via WordPress or download the plugin and:

1. Upload the plugin files to the `/wp-content/plugins/media-library-file-size` directory.
1. Activate the plugin through the 'Plugins' screen in WordPress.
1. Navigate to the Media Library and click the Index Media button.

== Screenshots ==

1. The Media Library view with the new File Size column and 'Index Media' button.
2. Pressing this button indexes your Media Library file sizes.

== Frequently Asked Questions ==

= The file size does not show for an attachment in the media library? =

First try to index the Media Library by pressing the button 'Index Media' (when viewing the Media Library in list view mode). If this fails, it usually means that the file does not exist locally on the server.

The most common reason is because the file has been offloaded onto a CDN. 

= I do not see a Index Media button? =

Make sure you are looking at your Media Library, and you are in List view. Grid mode does not work with this plugin.

= What is the additional file size e.g. ‘(+27 KB)’ in the file size column? =

This is a collective size of your thumbnails (and other sized images).

== Changelog ==

= 1.3 =
* Spelling fix
* When uninstalling the plugin, it removes the post meta we use to index the files.
* Readme.txt updates
* Index check -- do not show 'Index Media' button if the library is already indexed (also fixes first time arrow).

= 1.2 =
* Added arrow and redirect when plugin activated to help users press the Index Media button

= 1.1 =
* Updated to work with WordPress 4.1+

= 1.0 =
* Initial release.

== Upgrade Notice ==
