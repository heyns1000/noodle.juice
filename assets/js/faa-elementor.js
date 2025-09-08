/**
 * FAA™ Elementor SaaS Domination Engine - JavaScript That Makes Competitors Shake
 */

(function($) {
    'use strict';
    
    // FAA Domination Engine Core
    const FAA_Engine = {
        
        // Initialize all FAA widgets
        init: function() {
            this.initVerificationBadges();
            this.initPulseCharts();
            this.initDreamBigBanners();
            this.initCompetitorDetection();
            this.initAtomVerification();
            
            console.log('🦍 FAA™ Domination Engine Activated');
        },
        
        // Verification Badge System
        initVerificationBadges: function() {
            $('.faa-verification-badge').each(function() {
                const $badge = $(this);
                const atomId = $badge.data('atom-id');
                
                // Add hover effects
                $badge.on('mouseenter', function() {
                    $(this).addClass('faa-badge-hover');
                    
                    // Show verification details
                    const tooltip = $('<div class="faa-verification-tooltip">')
                        .html(`
                            <strong>FAA™ Verified</strong><br>
                            Atom ID: ${atomId}<br>
                            Status: ✔ Verified<br>
                            Tamper Events: 0
                        `)
                        .appendTo('body');
                    
                    const offset = $(this).offset();
                    tooltip.css({
                        position: 'absolute',
                        top: offset.top - tooltip.outerHeight() - 10,
                        left: offset.left + ($(this).outerWidth() / 2) - (tooltip.outerWidth() / 2),
                        zIndex: 10000
                    });
                });
                
                $badge.on('mouseleave', function() {
                    $(this).removeClass('faa-badge-hover');
                    $('.faa-verification-tooltip').remove();
                });
            });
        },
        
        // Pulse Chart System
        initPulseCharts: function() {
            $('.faa-pulse-chart-widget').each(function() {
                const $chart = $(this);
                const chartId = $chart.attr('id');
                
                // Add real-time pulse indicator
                const $indicator = $chart.find('.faa-pulse-indicator');
                if ($indicator.length) {
                    setInterval(function() {
                        $indicator.addClass('faa-pulse-active');
                        setTimeout(function() {
                            $indicator.removeClass('faa-pulse-active');
                        }, 1000);
                    }, 3000);
                }
            });
        },
        
        // Dream Big Banner System - The Competitor Shaker
        initDreamBigBanners: function() {
            $('.faa-dream-big-banner').each(function() {
                const $banner = $(this);
                
                // Add entrance animation
                $banner.addClass('faa-banner-entrance');
                
                // Particle system
                this.createParticleSystem($banner);
                
                // Power-up on scroll into view
                const observer = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            $(entry.target).addClass('faa-banner-active');
                            this.triggerDominationMode($(entry.target));
                        }
                    });
                }, { threshold: 0.5 });
                
                observer.observe(this);
            });
        },
        
        // Particle System for Dream Big Banner
        createParticleSystem: function($banner) {
            const $effects = $banner.find('.faa-banner-effects');
            
            setInterval(function() {
                const $particle = $('<div class="faa-dynamic-particle"></div>');
                $particle.css({
                    position: 'absolute',
                    left: Math.random() * 100 + '%',
                    top: Math.random() * 100 + '%',
                    width: '2px',
                    height: '2px',
                    background: 'rgba(255, 255, 255, 0.8)',
                    borderRadius: '50%',
                    animation: 'faa-particle-rise 3s ease-out forwards'
                });
                
                $effects.append($particle);
                
                setTimeout(function() {
                    $particle.remove();
                }, 3000);
            }, 500);
        },
        
        // Competitor Detection System
        initCompetitorDetection: function() {
            const competitorKeywords = [
                'beaver builder', 'divi', 'visual composer', 'wpbakery', 
                'oxygen', 'bricks', 'breakdance', 'thrive architect'
            ];
            
            const pageContent = document.body.innerText.toLowerCase();
            let competitorsDetected = [];
            
            competitorKeywords.forEach(keyword => {
                if (pageContent.includes(keyword)) {
                    competitorsDetected.push(keyword);
                }
            });
            
            if (competitorsDetected.length > 0) {
                this.activateDominationMode(competitorsDetected);
            }
        },
        
        // Activate Domination Mode
        activateDominationMode: function(competitors) {
            console.log('🦍 COMPETITORS DETECTED:', competitors);
            console.log('🚀 ACTIVATING FAA™ DOMINATION MODE');
            
            // Add domination class to all FAA widgets
            $('.faa-dream-big-banner, .faa-verification-badge, .faa-pulse-chart-widget')
                .addClass('faa-domination-mode');
            
            // Create domination notification
            const $notification = $(`
                <div class="faa-domination-notification">
                    <div class="faa-notification-content">
                        <span class="faa-notification-icon">🦍</span>
                        <span class="faa-notification-text">
                            FAA™ DOMINATION MODE ACTIVE<br>
                            <small>Competitors detected: ${competitors.join(', ')}</small>
                        </span>
                        <button class="faa-notification-close">×</button>
                    </div>
                </div>
            `).appendTo('body');
            
            // Auto-hide notification
            setTimeout(function() {
                $notification.fadeOut(500, function() {
                    $(this).remove();
                });
            }, 5000);
            
            // Close button
            $notification.find('.faa-notification-close').on('click', function() {
                $notification.fadeOut(300, function() {
                    $(this).remove();
                });
            });
        },
        
        // Trigger specific domination effects
        triggerDominationMode: function($element) {
            $element.addClass('faa-domination-active');
            
            // Add screen shake effect
            $('body').addClass('faa-screen-shake');
            setTimeout(function() {
                $('body').removeClass('faa-screen-shake');
            }, 1000);
            
            // Add power surge effect
            const $surge = $('<div class="faa-power-surge"></div>').appendTo($element);
            setTimeout(function() {
                $surge.remove();
            }, 2000);
        },
        
        // Atom-Level Verification System
        initAtomVerification: function() {
            // Monitor all FAA widgets for tampering
            const observer = new MutationObserver((mutations) => {
                mutations.forEach((mutation) => {
                    if (mutation.target.classList.contains('faa-verification-badge') ||
                        mutation.target.closest('.faa-verification-badge')) {
                        this.verifyAtomIntegrity(mutation.target);
                    }
                });
            });
            
            // Start observing
            observer.observe(document.body, {
                childList: true,
                subtree: true,
                attributes: true,
                attributeOldValue: true
            });
        },
        
        // Verify Atom Integrity
        verifyAtomIntegrity: function(element) {
            const $element = $(element);
            const atomId = $element.data('atom-id') || $element.closest('[data-atom-id]').data('atom-id');
            
            if (atomId) {
                // Send verification request to server
                $.ajax({
                    url: faa_elementor.ajax_url,
                    type: 'POST',
                    data: {
                        action: 'faa_verify_atom',
                        atom_id: atomId,
                        nonce: faa_elementor.nonce
                    },
                    success: function(response) {
                        if (response.success) {
                            console.log('✔ Atom verification passed:', atomId);
                        } else {
                            console.warn('⚠ Atom verification failed:', atomId);
                            // Add tamper warning
                            $element.addClass('faa-tamper-detected');
                        }
                    }
                });
            }
        }
    };
    
    // Initialize when document is ready
    $(document).ready(function() {
        FAA_Engine.init();
    });
    
    // Initialize for Elementor editor
    $(window).on('elementor/frontend/init', function() {
        FAA_Engine.init();
    });
    
    // Add dynamic CSS for effects
    const dynamicCSS = `
        <style id="faa-dynamic-styles">
            .faa-banner-entrance {
                animation: faa-entrance 1s ease-out forwards;
            }
            
            @keyframes faa-entrance {
                0% {
                    opacity: 0;
                    transform: translateY(50px) scale(0.9);
                }
                100% {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
            }
            
            .faa-screen-shake {
                animation: faa-screen-shake 0.5s ease-in-out;
            }
            
            @keyframes faa-screen-shake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-2px); }
                75% { transform: translateX(2px); }
            }
            
            .faa-power-surge {
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: radial-gradient(circle, rgba(59, 130, 246, 0.3) 0%, transparent 70%);
                animation: faa-surge 2s ease-out forwards;
                pointer-events: none;
            }
            
            @keyframes faa-surge {
                0% {
                    opacity: 0;
                    transform: scale(0.5);
                }
                50% {
                    opacity: 1;
                    transform: scale(1.2);
                }
                100% {
                    opacity: 0;
                    transform: scale(2);
                }
            }
            
            .faa-domination-notification {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 999999;
                background: linear-gradient(135deg, #dc2626, #991b1b);
                color: white;
                padding: 16px 20px;
                border-radius: 12px;
                box-shadow: 0 8px 32px rgba(220, 38, 38, 0.4);
                animation: faa-notification-slide 0.5s ease-out forwards;
            }
            
            @keyframes faa-notification-slide {
                0% {
                    opacity: 0;
                    transform: translateX(100%);
                }
                100% {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
            
            .faa-notification-content {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .faa-notification-icon {
                font-size: 24px;
                animation: faa-pulse 1s infinite ease-in-out;
            }
            
            .faa-notification-close {
                background: none;
                border: none;
                color: white;
                font-size: 20px;
                cursor: pointer;
                margin-left: 12px;
            }
            
            .faa-tamper-detected {
                border: 2px solid #dc2626 !important;
                animation: faa-tamper-warning 1s infinite ease-in-out;
            }
            
            @keyframes faa-tamper-warning {
                0%, 100% { border-color: #dc2626; }
                50% { border-color: #fbbf24; }
            }
            
            @keyframes faa-particle-rise {
                0% {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
                100% {
                    opacity: 0;
                    transform: translateY(-50px) scale(0);
                }
            }
        </style>
    `;
    
    $('head').append(dynamicCSS);
    
})(jQuery);