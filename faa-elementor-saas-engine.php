<?php
/**
 * Plugin Name: FAA™ Elementor SaaS Domination Engine™
 * Description: Planetary-grade Elementor widgets that make competitors shake. Atom-level verified, scroll-sealed, sovereignty-guaranteed.
 * Version: FAA8000-ELE-1.0
 * Author: FAA Quantum UI Department™
 * License: FAA Master License Agreement
 * Text Domain: faa-elementor-engine
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// Define plugin constants
define('FAA_ELEMENTOR_VERSION', 'FAA8000-ELE-1.0');
define('FAA_ELEMENTOR_URL', plugin_dir_url(__FILE__));
define('FAA_ELEMENTOR_PATH', plugin_dir_path(__FILE__));

/**
 * Main FAA Elementor Engine Class
 */
class FAA_Elementor_Engine {
    
    private static $_instance = null;
    
    public static function instance() {
        if (is_null(self::$_instance)) {
            self::$_instance = new self();
        }
        return self::$_instance;
    }
    
    public function __construct() {
        add_action('init', [$this, 'init']);
        add_action('plugins_loaded', [$this, 'plugins_loaded']);
    }
    
    public function init() {
        // Load text domain
        load_plugin_textdomain('faa-elementor-engine');
        
        // Initialize widgets
        add_action('elementor/widgets/widgets_registered', [$this, 'register_widgets']);
        add_action('elementor/elements/categories_registered', [$this, 'register_categories']);
        
        // Enqueue scripts and styles
        add_action('wp_enqueue_scripts', [$this, 'enqueue_scripts']);
        add_action('elementor/editor/before_enqueue_scripts', [$this, 'editor_scripts']);
    }
    
    public function plugins_loaded() {
        // Check if Elementor is installed and activated
        if (!did_action('elementor/loaded')) {
            add_action('admin_notices', [$this, 'admin_notice_missing_elementor']);
            return;
        }
        
        // Check for minimum Elementor version
        if (!version_compare(ELEMENTOR_VERSION, '3.0.0', '>=')) {
            add_action('admin_notices', [$this, 'admin_notice_minimum_elementor_version']);
            return;
        }
    }
    
    public function register_categories($elements_manager) {
        $elements_manager->add_category(
            'faa-domination',
            [
                'title' => __('🦍 FAA™ Domination Widgets', 'faa-elementor-engine'),
                'icon' => 'fa fa-crown',
            ]
        );
    }
    
    public function register_widgets() {
        // Register all FAA widgets
        require_once FAA_ELEMENTOR_PATH . 'widgets/faa-verification-badge.php';
        require_once FAA_ELEMENTOR_PATH . 'widgets/faa-pulse-chart.php';
        require_once FAA_ELEMENTOR_PATH . 'widgets/faa-scroll-ledger.php';
        require_once FAA_ELEMENTOR_PATH . 'widgets/faa-sovereign-lock.php';
        require_once FAA_ELEMENTOR_PATH . 'widgets/faa-omnidrop-showcase.php';
        require_once FAA_ELEMENTOR_PATH . 'widgets/faa-brand-pulse.php';
        require_once FAA_ELEMENTOR_PATH . 'widgets/faa-atomic-counter.php';
        require_once FAA_ELEMENTOR_PATH . 'widgets/faa-dream-big-banner.php';
        
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new \FAA_Verification_Badge());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new \FAA_Pulse_Chart());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new \FAA_Scroll_Ledger());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new \FAA_Sovereign_Lock());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new \FAA_OmniDrop_Showcase());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new \FAA_Brand_Pulse());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new \FAA_Atomic_Counter());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new \FAA_Dream_Big_Banner());
    }
    
    public function enqueue_scripts() {
        wp_enqueue_style(
            'faa-elementor-engine',
            FAA_ELEMENTOR_URL . 'assets/css/faa-elementor.css',
            [],
            FAA_ELEMENTOR_VERSION
        );
        
        wp_enqueue_script(
            'faa-elementor-engine',
            FAA_ELEMENTOR_URL . 'assets/js/faa-elementor.js',
            ['jquery'],
            FAA_ELEMENTOR_VERSION,
            true
        );
        
        wp_localize_script('faa-elementor-engine', 'faa_elementor', [
            'ajax_url' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('faa_elementor_nonce'),
            'version' => FAA_ELEMENTOR_VERSION,
            'atom_id' => 'FAA-' . time() . '-' . wp_generate_password(8, false)
        ]);
    }
    
    public function editor_scripts() {
        wp_enqueue_script(
            'faa-elementor-editor',
            FAA_ELEMENTOR_URL . 'assets/js/faa-editor.js',
            ['elementor-editor'],
            FAA_ELEMENTOR_VERSION,
            true
        );
    }
    
    public function admin_notice_missing_elementor() {
        if (isset($_GET['activate'])) unset($_GET['activate']);
        
        $message = sprintf(
            esc_html__('"%1$s" requires "%2$s" to be installed and activated.', 'faa-elementor-engine'),
            '<strong>' . esc_html__('FAA™ Elementor SaaS Domination Engine™', 'faa-elementor-engine') . '</strong>',
            '<strong>' . esc_html__('Elementor', 'faa-elementor-engine') . '</strong>'
        );
        
        printf('<div class="notice notice-warning is-dismissible"><p>%1$s</p></div>', $message);
    }
    
    public function admin_notice_minimum_elementor_version() {
        if (isset($_GET['activate'])) unset($_GET['activate']);
        
        $message = sprintf(
            esc_html__('"%1$s" requires "%2$s" version %3$s or greater.', 'faa-elementor-engine'),
            '<strong>' . esc_html__('FAA™ Elementor SaaS Domination Engine™', 'faa-elementor-engine') . '</strong>',
            '<strong>' . esc_html__('Elementor', 'faa-elementor-engine') . '</strong>',
            '3.0.0'
        );
        
        printf('<div class="notice notice-warning is-dismissible"><p>%1$s</p></div>', $message);
    }
}

// Initialize the plugin
FAA_Elementor_Engine::instance();

/**
 * FAA Atom-Level Verification Functions
 */
function faa_generate_atom_id() {
    return 'FAA-ATOM-' . time() . '-' . wp_generate_password(12, false);
}

function faa_verify_scroll($content, $user_id = null) {
    $atom_id = faa_generate_atom_id();
    $timestamp = current_time('mysql');
    $user_id = $user_id ?: get_current_user_id();
    
    // Store verification in database
    global $wpdb;
    $table_name = $wpdb->prefix . 'faa_scroll_ledger';
    
    $wpdb->insert(
        $table_name,
        [
            'atom_id' => $atom_id,
            'content_hash' => md5($content),
            'user_id' => $user_id,
            'timestamp' => $timestamp,
            'status' => 'verified',
            'tamper_events' => 0
        ]
    );
    
    return $atom_id;
}

function faa_get_verification_badge($atom_id) {
    return '<span class="faa-verification-badge" data-atom-id="' . esc_attr($atom_id) . '">
        ✔ Verified | FAA Atom ID: #' . esc_html($atom_id) . '
    </span>';
}

/**
 * Create FAA Scroll Ledger Table on Activation
 */
register_activation_hook(__FILE__, 'faa_create_scroll_ledger_table');

function faa_create_scroll_ledger_table() {
    global $wpdb;
    
    $table_name = $wpdb->prefix . 'faa_scroll_ledger';
    
    $charset_collate = $wpdb->get_charset_collate();
    
    $sql = "CREATE TABLE $table_name (
        id mediumint(9) NOT NULL AUTO_INCREMENT,
        atom_id varchar(100) NOT NULL,
        content_hash varchar(32) NOT NULL,
        user_id bigint(20) NOT NULL,
        timestamp datetime DEFAULT CURRENT_TIMESTAMP NOT NULL,
        status varchar(20) DEFAULT 'verified' NOT NULL,
        tamper_events int(11) DEFAULT 0 NOT NULL,
        signature text,
        PRIMARY KEY (id),
        UNIQUE KEY atom_id (atom_id)
    ) $charset_collate;";
    
    require_once(ABSPATH . 'wp-admin/includes/upgrade.php');
    dbDelta($sql);
}