<?php
/**
 * FAA Verification Badge Widget
 */

if (!defined('ABSPATH')) {
    exit;
}

class FAA_Verification_Badge extends \Elementor\Widget_Base {
    
    public function get_name() {
        return 'faa-verification-badge';
    }
    
    public function get_title() {
        return __('🛡️ FAA™ Verification Badge', 'faa-elementor-engine');
    }
    
    public function get_icon() {
        return 'eicon-shield-check';
    }
    
    public function get_categories() {
        return ['faa-domination'];
    }
    
    public function get_keywords() {
        return ['faa', 'verification', 'badge', 'security', 'atom'];
    }
    
    protected function register_controls() {
        
        $this->start_controls_section(
            'content_section',
            [
                'label' => __('🧬 Atom Verification Settings', 'faa-elementor-engine'),
                'tab' => \Elementor\Controls_Manager::TAB_CONTENT,
            ]
        );
        
        $this->add_control(
            'verification_text',
            [
                'label' => __('Verification Text', 'faa-elementor-engine'),
                'type' => \Elementor\Controls_Manager::TEXT,
                'default' => __('FAA™ Verified Content', 'faa-elementor-engine'),
                'placeholder' => __('Enter your verified content', 'faa-elementor-engine'),
            ]
        );
        
        $this->add_control(
            'badge_style',
            [
                'label' => __('Badge Style', 'faa-elementor-engine'),
                'type' => \Elementor\Controls_Manager::SELECT,
                'default' => 'sovereign',
                'options' => [
                    'sovereign' => __('🦍 Sovereign Gold', 'faa-elementor-engine'),
                    'atomic' => __('🧬 Atomic Blue', 'faa-elementor-engine'),
                    'quantum' => __('⚡ Quantum Purple', 'faa-elementor-engine'),
                    'dream-big' => __('✨ Dream Big Green', 'faa-elementor-engine'),
                ],
            ]
        );
        
        $this->add_control(
            'show_atom_id',
            [
                'label' => __('Show Atom ID', 'faa-elementor-engine'),
                'type' => \Elementor\Controls_Manager::SWITCHER,
                'label_on' => __('Show', 'faa-elementor-engine'),
                'label_off' => __('Hide', 'faa-elementor-engine'),
                'return_value' => 'yes',
                'default' => 'yes',
            ]
        );
        
        $this->add_control(
            'show_timestamp',
            [
                'label' => __('Show Timestamp', 'faa-elementor-engine'),
                'type' => \Elementor\Controls_Manager::SWITCHER,
                'label_on' => __('Show', 'faa-elementor-engine'),
                'label_off' => __('Hide', 'faa-elementor-engine'),
                'return_value' => 'yes',
                'default' => 'yes',
            ]
        );
        
        $this->end_controls_section();
        
        // Style Section
        $this->start_controls_section(
            'style_section',
            [
                'label' => __('🎨 Badge Styling', 'faa-elementor-engine'),
                'tab' => \Elementor\Controls_Manager::TAB_STYLE,
            ]
        );
        
        $this->add_control(
            'badge_size',
            [
                'label' => __('Badge Size', 'faa-elementor-engine'),
                'type' => \Elementor\Controls_Manager::SLIDER,
                'size_units' => ['px', 'em', 'rem'],
                'range' => [
                    'px' => [
                        'min' => 10,
                        'max' => 100,
                        'step' => 1,
                    ],
                ],
                'default' => [
                    'unit' => 'px',
                    'size' => 16,
                ],
                'selectors' => [
                    '{{WRAPPER}} .faa-verification-badge' => 'font-size: {{SIZE}}{{UNIT}};',
                ],
            ]
        );
        
        $this->end_controls_section();
    }
    
    protected function render() {
        $settings = $this->get_settings_for_display();
        
        // Generate atom ID for this verification
        $atom_id = faa_generate_atom_id();
        $timestamp = current_time('Y-m-d H:i:s');
        
        // Verify the content
        faa_verify_scroll($settings['verification_text']);
        
        $badge_class = 'faa-verification-badge faa-badge-' . $settings['badge_style'];
        
        echo '<div class="faa-verification-widget">';
        echo '<div class="faa-verified-content">';
        echo '<span class="faa-content-text">' . esc_html($settings['verification_text']) . '</span>';
        echo '<div class="' . esc_attr($badge_class) . '" data-atom-id="' . esc_attr($atom_id) . '">';
        echo '<span class="faa-check-icon">✔</span>';
        echo '<span class="faa-verified-text">FAA™ Verified</span>';
        
        if ($settings['show_atom_id'] === 'yes') {
            echo '<span class="faa-atom-id">Atom ID: #' . esc_html(substr($atom_id, -8)) . '</span>';
        }
        
        if ($settings['show_timestamp'] === 'yes') {
            echo '<span class="faa-timestamp">' . esc_html($timestamp) . '</span>';
        }
        
        echo '</div>';
        echo '</div>';
        echo '</div>';
    }
    
    protected function content_template() {
        ?>
        <#
        var atomId = 'FAA-PREVIEW-' + Math.random().toString(36).substr(2, 8);
        var timestamp = new Date().toISOString().slice(0, 19).replace('T', ' ');
        var badgeClass = 'faa-verification-badge faa-badge-' + settings.badge_style;
        #>
        <div class="faa-verification-widget">
            <div class="faa-verified-content">
                <span class="faa-content-text">{{{ settings.verification_text }}}</span>
                <div class="{{ badgeClass }}" data-atom-id="{{ atomId }}">
                    <span class="faa-check-icon">✔</span>
                    <span class="faa-verified-text">FAA™ Verified</span>
                    <# if (settings.show_atom_id === 'yes') { #>
                        <span class="faa-atom-id">Atom ID: #{{ atomId.substr(-8) }}</span>
                    <# } #>
                    <# if (settings.show_timestamp === 'yes') { #>
                        <span class="faa-timestamp">{{ timestamp }}</span>
                    <# } #>
                </div>
            </div>
        </div>
        <?php
    }
}