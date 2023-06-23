<?php
/*
Plugin Name: Media Library File Size
Plugin URI: https://ss88.us/plugins/media-library-file-size
Description: Creates a new column in your Media Library to show you the file (and collective images) size of files!
Version: 1.3
Author: SS88 LLC
Author URI: https://ss88.us
*/

class SS88_MediaLibraryFileSize {

    protected $version = 1.3;

    public static function init() {

        $C = __CLASS__;
        new $C;

    }

    function __construct() {

        global $pagenow;

		register_uninstall_hook(__FILE__, ['SS88_MediaLibraryFileSize', 'register_uninstall_hook']);

        if($pagenow=='upload.php') {

            add_filter('manage_media_custom_column', [$this, 'manage_media_custom_column'], 10, 2);
            add_filter('manage_media_columns', [$this, 'manage_media_columns']);

            add_action('manage_upload_sortable_columns', [$this, 'manage_upload_sortable_columns']);
            add_action('pre_get_posts', [$this, 'pre_get_posts']);
            add_action('admin_enqueue_scripts', [$this, 'admin_enqueue_scripts']);

        }

        if(is_admin()) {

            add_action('wp_ajax_SS88MLFS_index', [$this, 'index']);
			add_action('wp_ajax_SS88MLFS_indexCount', [$this, 'indexCount']);

        }

		add_filter('wp_generate_attachment_metadata', [$this, 'wp_generate_attachment_metadata'], PHP_INT_MAX, 2);
        add_filter('plugin_action_links_' . plugin_basename(__FILE__), [$this, 'plugin_action_links']);

		add_action('activated_plugin', [$this, 'activated_plugin']);

    }

	public static function activated_plugin($plugin) {

		if($plugin == 'media-library-file-size/ss88-media-library-file-size.php') {

			wp_safe_redirect(admin_url('upload.php?mode=list&ss88first'));
			exit;

		}

	}

    function plugin_action_links($actions) {
        $mylinks = [
            '<a href="https://wordpress.org/support/plugin/media-library-file-size/" target="_blank">Need help?</a>',
        ];
        return array_merge( $actions, $mylinks );
    }

    function admin_enqueue_scripts() {

        wp_enqueue_script('noty', plugin_dir_url( __FILE__ ) . 'assets/js/noty.js', false, $this->version);
        wp_enqueue_script('SS88_MLFS-media', plugin_dir_url( __FILE__ ) . 'assets/js/media.js', ['noty'], $this->version);
        wp_localize_script('SS88_MLFS-media', 'ss88', array('ajax_url' => admin_url( 'admin-ajax.php' )));

        wp_enqueue_style('noty', plugin_dir_url( __FILE__ ) . 'assets/css/noty.css', false, $this->version);
        wp_enqueue_style('SS88_MLFS-media', plugin_dir_url( __FILE__ ) . 'assets/css/media.css', false, $this->version);

    }

    function index() {

        $returnData = [];

        $attachments = get_posts([
            'post_type' => 'attachment',
            'numberposts' => -1,
            'meta_query' => [
                [
                    'key' => 'SS88MLFS',
                    'compare' => 'NOT EXISTS'
                ],
            ]
        ]);

        $CompletedCount = 0;

        if($attachments) {

            foreach($attachments as $attachment) {

                $metadata = wp_get_attachment_metadata($attachment->ID);

                // if(!isset($metadata['filesize'])) {

                //     $file = get_attached_file($attachment->ID);

                //     if(file_exists($file)) {

                //         $metadata = wp_generate_attachment_metadata($attachment->ID, $file);
                //         wp_update_attachment_metadata($attachment->ID, $metadata);

                //     }

                // }

                if($this->updateSize($metadata, $attachment->ID)) {

                    $CompletedCount++;

                    $returnData[] = [
                        'attachment_id' => $attachment->ID,
                        'html' => $this->outputHTML($attachment->ID)
                    ];
        
                }

            }

            if($CompletedCount) {
                
                wp_send_json_success([
                    'html' => $returnData,
                    'message' => 'You just indexed '. $CompletedCount .' attachments. Your media library has been indexed.'
                ]);
            
            }
            else wp_send_json_error(['httpcode' => 99, 'body' => 'No attachments were indexed. This usually means they exist, but the file(s) are not on the local server.']);

        }
        else {

            wp_send_json_error(['httpcode' => -1, 'body' => 'There are no attachments to index.']);

        }

        echo count($attachments);

    }

	function indexCount() {

        $returnData = [];

        $attachments = get_posts([
            'post_type' => 'attachment',
            'numberposts' => -1,
            'meta_query' => [
                [
                    'key' => 'SS88MLFS',
                    'compare' => 'NOT EXISTS'
                ],
            ]
        ]);

		if($attachments) wp_send_json_success();
		else return wp_send_json_error();

	}

    function wp_generate_attachment_metadata($data, $attachment_id) {

        $this->updateSize($data, $attachment_id);

        return $data;

    }

    function manage_upload_sortable_columns($columns) {

        $columns['SS88_MediaLibraryFileSize'] = 'SS88_MediaLibraryFileSize';
        
        return $columns;

    }

	function manage_media_columns($columns) {

		$columns['SS88_MediaLibraryFileSize'] = __('File Size');
		
		return $columns;
	
	}

	function manage_media_custom_column($columnName, $postID) {

        if($columnName == 'SS88_MediaLibraryFileSize') {

			echo $this->outputHTML($postID);

        }

	}

    function pre_get_posts($query) {

        if(!empty($_REQUEST['orderby']) && $_REQUEST['orderby'] == 'SS88_MediaLibraryFileSize') {

            $query->set('order', ($_REQUEST['order']=='asc') ? 'asc' : 'desc');
            $query->set('orderby', 'meta_value_num');
            $query->set('meta_key', 'SS88MLFS');

        }

    }

    function updateSize($data, $attachment_id) {

        $Size = 0;
		$File = get_attached_file($attachment_id);

        if(isset($data['filesize'])) {

            $Size = $data['filesize'];

        }

        if($Size===0 && file_exists($File)) {

            $Size = filesize($File);

        }

        if($Size) {

            update_post_meta($attachment_id, 'SS88MLFS', $Size);

        }

        return $Size;

    }

    function outputHTML($attachment_id) {

        $html = '';

        $file = get_attached_file($attachment_id);
        $Variants = wp_get_attachment_metadata($attachment_id);
        $VariantSize = 0;

        if(isset($Variants['sizes'])) {

            foreach($Variants['sizes'] as $Variant) {

                $VariantSize += isset($Variant['filesize']) ? $Variant['filesize'] : filesize( pathinfo($file, PATHINFO_DIRNAME) . '/' . $Variant['file'] );

            }

        }

        $ExtaHTML = ($VariantSize) ? '<small>(+'. size_format($VariantSize) .')</small>' : '';
        $MetaSize = get_post_meta($attachment_id, 'SS88MLFS', true);
        $FinalSize = isset($Variants['filesize']) ? $Variants['filesize'] : $MetaSize;

        if($FinalSize) {

            $html = size_format($FinalSize) . $ExtaHTML;

        }

        return $html;

    }

	public static function register_uninstall_hook() {
		
		delete_post_meta_by_key('SS88MLFS');
		
	}

	function debug($msg) {

		error_log("\n" . '[' . date('Y-m-d H:i:s') . '] ' .  $msg, 3, plugin_dir_path(__FILE__) . 'debug.log');

	}

}

add_action('plugins_loaded', ['SS88_MediaLibraryFileSize', 'init']);
add_action('activated_plugin', ['SS88_MediaLibraryFileSize', 'activated_plugin']);