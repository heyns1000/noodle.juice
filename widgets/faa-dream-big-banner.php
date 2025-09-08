<?php
/**
 * FAA Dream Big Banner Widget - The signature widget that makes competitors shake
 */

if (!defined('ABSPATH')) {
    exit;
}

class FAA_Dream_Big_Banner extends \Elementor\Widget_Base {
    
    public function get_name() {
        return 'faa-dream-big-banner';
    }
    
    public function get_title() {
        return __('✨ FAA™ Dream Big Banner', 'faa-elementor-engine');
    }
    
    public function get_icon() {
        return 'eicon-banner';
    }
    
    public function get_categories() {
        return ['faa-domination'];
    }
    
    public function get_keywords() {
        return ['faa', 'dream', 'big', 'banner', 'signature'];
    }
    
    protected function register_controls() {
        
        $this->start_controls_section(
            'banner_content',
            [
                'label' => __('✨ Dream Big Settings', 'faa-elementor-engine'),
                'tab' => \Elementor\Controls_Manager::TAB_CONTENT,
            ]
        );
        
        $this->add_control(
            'banner_text',
            [
                'label' => __('Banner Text', 'faa-elementor-engine'),
                'type' => \Elementor\Controls_Manager::TEXT,
                'default' => __('DREAM BIG', 'faa-elementor-engine'),
            ]
        );
        
        $this->add_control(
            'subtitle_text',
            [
                'label' => __('Subtitle', 'faa-elementor-engine'),
                'type' => \Elementor\Controls_Manager::TEXT,
                'default' => __('Every Plugin Must Dream Big™', 'faa-elementor-engine'),
            ]
        );
        
        $this->add_control(
            'banner_style',
            [
                'label' => __('Banner Style', 'faa-elementor-engine'),
                'type' => \Elementor\Controls_Manager::SELECT,
                'default' => 'sovereign',
                'options' => [
                    'sovereign' => __('🦍 Sovereign Power', 'faa-elementor-engine'),
                    'atomic' => __('🧬 Atomic Energy', 'faa-elementor-engine'),
                    'quantum' => __('⚡ Quantum Field', 'faa-elementor-engine'),
                    'omnidrop' => __('🚀 OmniDrop Mode', 'faa-elementor-engine'),
                ],
            ]
        );
        
        $this->add_control(
            'show_mascot',
            [
                'label' => __('Show Dream Mascot', 'faa-elementor-engine'),
                'type' => \Elementor\Controls_Manager::SWITCHER,
                'label_on' => __('Show', 'faa-elementor-engine'),
                'label_off' => __('Hide', 'faa-elementor-engine'),
                'return_value' => 'yes',
                'default' => 'yes',
            ]
        );
        
        $this->add_control(
            'animation_type',
            [
                'label' => __('Animation', 'faa-elementor-engine'),
                'type' => \Elementor\Controls_Manager::SELECT,
                'default' => 'pulse',
                'options' => [
                    'none' => __('None', 'faa-elementor-engine'),
                    'pulse' => __('🔥 Pulse', 'faa-elementor-engine'),
                    'glow' => __('✨ Glow', 'faa-elementor-engine'),
                    'shake' => __('⚡ Power Shake', 'faa-elementor-engine'),
                    'dominate' => __('🦍 Domination Mode', 'faa-elementor-engine'),
                ],
            ]
        );
        
        $this->end_controls_section();
        
        // Style Section
        $this->start_controls_section(
            'banner_style_section',
            [
                'label' => __('🎨 Banner Styling', 'faa-elementor-engine'),
                'tab' => \Elementor\Controls_Manager::TAB_STYLE,
            ]
        );
        
        $this->add_control(
            'text_color',
            [
                'label' => __('Text Color', 'faa-elementor-engine'),
                'type' => \Elementor\Controls_Manager::COLOR,
                'default' => '#ffffff',
                'selectors' => [
                    '{{WRAPPER}} .faa-dream-big-text' => 'color: {{VALUE}};',
                ],
            ]
        );
        
        $this->add_control(
            'background_gradient',
            [
                'label' => __('Background Gradient', 'faa-elementor-engine'),
                'type' => \Elementor\Controls_Manager::COLOR,
                'default' => '#3b82f6',
            ]
        );
        
        $this->end_controls_section();
    }
    
    protected function render() {
        $settings = $this->get_settings_for_display();
        $widget_id = $this->get_id();
        
        $banner_classes = [
            'faa-dream-big-banner',
            'faa-banner-' . $settings['banner_style'],
            'faa-animation-' . $settings['animation_type']
        ];
        
        echo '<div class="' . esc_attr(implode(' ', $banner_classes)) . '" id="faa-banner-' . esc_attr($widget_id) . '">';
        
        if ($settings['show_mascot'] === 'yes') {
            echo '<div class="faa-dream-mascot">';
            echo '<div class="faa-mascot-eye"></div>';
            echo '<div class="faa-mascot-cape">DREAM BIG</div>';
            echo '</div>';
        }
        
        echo '<div class="faa-banner-content">';
        echo '<h1 class="faa-dream-big-text">' . esc_html($settings['banner_text']) . '</h1>';
        echo '<p class="faa-banner-subtitle">' . esc_html($settings['subtitle_text']) . '</p>';
        echo '<div class="faa-verification-seal">';
        echo '<span class="faa-seal-icon">🛡️</span>';
        echo '<span class="faa-seal-text">FAA™ Verified Dream Engine</span>';
        echo '</div>';
        echo '</div>';
        
        echo '<div class="faa-banner-effects">';
        for ($i = 0; $i < 5; $i++) {
            echo '<div class="faa-particle faa-particle-' . $i . '"></div>';
        }
        echo '</div>';
        
        echo '</div>';
        
        // Add competitive intimidation script
        ?>
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            const banner = document.getElementById('faa-banner-<?php echo esc_js($widget_id); ?>');
            
            // Competitive detection system
            const competitorKeywords = ['beaver builder', 'divi', 'visual composer', 'wpbakery', 'oxygen'];
            const pageContent = document.body.innerText.toLowerCase();
            
            let competitorDetected = false;
            competitorKeywords.forEach(keyword => {
                if (pageContent.includes(keyword)) {
                    competitorDetected = true;
                }
            });
            
            if (competitorDetected) {
                banner.classList.add('faa-domination-mode');
                console.log('🦍 FAA™ Domination Mode Activated - Competitors Detected');
                
                // Add intimidation effects
                setTimeout(() => {
                    banner.style.transform = 'scale(1.05)';
                    banner.style.boxShadow = '0 0 50px rgba(59, 130, 246, 0.8)';
                }, 1000);
            }
            
            // Dream Big pulse effect
            <?php if ($settings['animation_type'] === 'dominate'): ?>
            setInterval(() => {
                banner.style.animation = 'none';
                setTimeout(() => {
                    banner.style.animation = 'faa-dominate 3s ease-in-out';
                }, 10);
            }, 5000);
            <?php endif; ?>
        });
        </script>
        <?php
    }
}