#!/usr/bin/env python3
"""
Generate product sales website for Jimny Supercharger Kit
"""

import json
from pathlib import Path
from datetime import datetime


def generate_product_html():
    """Generate HTML for product sales page"""

    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Bolt-on Eaton M65 Supercharger Bracket Kit for Suzuki Jimny M13A. Massive torque gains, trail-proven performance.">
    <title>Jimny M65 Supercharger Kit - Smalltownboost</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary: #d32f2f;
            --secondary: #1976d2;
            --dark: #1a1a1a;
            --light: #f5f5f5;
            --text: #333;
            --border: #ddd;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            color: var(--text);
            line-height: 1.6;
            background: #fff;
        }

        /* Navigation */
        nav {
            background: var(--dark);
            color: white;
            padding: 15px 0;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .nav-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            font-size: 1.5em;
            font-weight: bold;
            color: var(--primary);
        }

        nav a {
            color: white;
            text-decoration: none;
            margin-left: 30px;
            transition: color 0.3s;
        }

        nav a:hover {
            color: var(--primary);
        }

        /* Hero Section */
        .hero {
            background: linear-gradient(135deg, var(--dark) 0%, #2a2a2a 100%);
            color: white;
            padding: 80px 20px;
            text-align: center;
        }

        .hero-content {
            max-width: 900px;
            margin: 0 auto;
        }

        .hero h1 {
            font-size: 3em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }

        .hero p {
            font-size: 1.3em;
            margin-bottom: 30px;
            opacity: 0.95;
        }

        .hero-badge {
            display: inline-block;
            background: var(--primary);
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
            margin-bottom: 30px;
        }

        .cta-button {
            background: var(--primary);
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 1.1em;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s, transform 0.2s;
            font-weight: bold;
            text-decoration: none;
            display: inline-block;
        }

        .cta-button:hover {
            background: #b71c1c;
            transform: translateY(-2px);
        }

        .cta-secondary {
            background: transparent;
            border: 2px solid white;
            margin-left: 15px;
        }

        .cta-secondary:hover {
            background: white;
            color: var(--primary);
        }

        /* Sections */
        section {
            max-width: 1200px;
            margin: 0 auto;
            padding: 60px 20px;
        }

        h2 {
            font-size: 2.2em;
            margin-bottom: 40px;
            color: var(--dark);
            text-align: center;
            position: relative;
            padding-bottom: 20px;
        }

        h2:after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 4px;
            background: var(--primary);
        }

        /* Features Grid */
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 30px;
            margin-top: 40px;
        }

        .feature-card {
            background: var(--light);
            padding: 30px;
            border-radius: 10px;
            border-left: 4px solid var(--primary);
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }

        .feature-icon {
            font-size: 2.5em;
            margin-bottom: 15px;
        }

        .feature-card h3 {
            margin-bottom: 10px;
            color: var(--primary);
        }

        /* Specs Section */
        .specs {
            background: var(--light);
        }

        .bom-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 40px;
        }

        .bom-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid var(--border);
        }

        .bom-card h4 {
            color: var(--primary);
            margin-bottom: 10px;
        }

        .bom-card ul {
            list-style: none;
            padding-left: 0;
        }

        .bom-card li {
            padding: 5px 0;
            border-bottom: 1px solid var(--border);
        }

        .bom-card li:last-child {
            border-bottom: none;
        }

        /* Pricing */
        .pricing-section {
            text-align: center;
        }

        .price-breakdown {
            background: white;
            border: 2px solid var(--primary);
            border-radius: 10px;
            padding: 40px;
            max-width: 500px;
            margin: 40px auto;
            box-shadow: 0 5px 20px rgba(211, 47, 47, 0.1);
        }

        .price-item {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid var(--border);
        }

        .price-item:last-child {
            border-bottom: none;
        }

        .price-total {
            font-size: 1.5em;
            font-weight: bold;
            color: var(--primary);
            margin-top: 20px;
            padding-top: 20px;
            border-top: 2px solid var(--primary);
        }

        .price-note {
            font-size: 0.9em;
            color: #666;
            margin-top: 15px;
            font-style: italic;
        }

        /* FAQ */
        .faq-section {
            background: var(--light);
        }

        .faq-grid {
            display: grid;
            gap: 20px;
            margin-top: 40px;
        }

        .faq-item {
            background: white;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid var(--secondary);
        }

        .faq-item h4 {
            color: var(--secondary);
            margin-bottom: 10px;
        }

        /* Contact Section */
        .contact-section {
            text-align: center;
            background: linear-gradient(135deg, var(--dark), #2a2a2a);
            color: white;
        }

        .contact-links {
            margin-top: 40px;
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
        }

        .contact-link {
            background: var(--primary);
            color: white;
            padding: 15px 30px;
            border-radius: 5px;
            text-decoration: none;
            font-weight: bold;
            transition: background 0.3s;
        }

        .contact-link:hover {
            background: #b71c1c;
        }

        /* Footer */
        footer {
            background: var(--dark);
            color: white;
            text-align: center;
            padding: 30px 20px;
            margin-top: 60px;
        }

        footer p {
            margin: 5px 0;
            opacity: 0.8;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .hero h1 {
                font-size: 2em;
            }

            .hero p {
                font-size: 1.1em;
            }

            .cta-button {
                display: block;
                margin: 10px 0;
            }

            .cta-secondary {
                margin-left: 0;
            }

            .nav-container {
                flex-direction: column;
                gap: 15px;
            }

            nav a {
                margin-left: 0;
            }

            .contact-links {
                flex-direction: column;
            }

            .contact-link {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav>
        <div class="nav-container">
            <div class="logo">🔥 Smalltownboost</div>
            <div>
                <a href="#features">Features</a>
                <a href="#specs">Specs</a>
                <a href="#pricing">Pricing</a>
                <a href="#faq">FAQ</a>
                <a href="#contact">Contact</a>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero">
        <div class="hero-content">
            <div class="hero-badge">🚙 TRAIL-PROVEN PERFORMANCE</div>
            <h1>Jimny M65 Supercharger Kit</h1>
            <p>Bolt-on power for your Suzuki Jimny M13A. Massive low-end torque. Instant throttle response. Proven in Alberta winters.</p>
            <div style="margin-top: 30px;">
                <button class="cta-button" onclick="document.getElementById('contact').scrollIntoView({behavior: 'smooth'})">Get Yours Today</button>
                <button class="cta-button cta-secondary" onclick="document.getElementById('specs').scrollIntoView({behavior: 'smooth'})">See Details</button>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section id="features">
        <h2>What You Get</h2>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">💥</div>
                <h3>Massive Torque</h3>
                <p>Instant low-end power that completely changes how your Jimny performs. Perfect for rock crawling and trails.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <h3>No Turbo Lag</h3>
                <p>Instant throttle response from a mechanical supercharger. No waiting. Just pure, immediate power delivery.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🏔️</div>
                <h3>Trail-Proven</h3>
                <p>Tested in real conditions: Alberta winters to +18°C, daily driving, and serious off-road use. It works.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🛠️</div>
                <h3>1-Day Install</h3>
                <p>If you're ready, this can be installed in a single day. Designed for simplicity and reliability.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">⚙️</div>
                <h3>Off-the-Shelf Parts</h3>
                <p>Uses the proven Eaton M65 supercharger. Rebuild kits are easy to find. Simple, reliable, easy to maintain.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <h3>Perfect Balance</h3>
                <p>The M65 is the sweet spot for the M13A. Great airflow without killing drivability or daily-ability.</p>
            </div>
        </div>
    </section>

    <!-- Specifications Section -->
    <section id="specs" class="specs">
        <h2>Complete Bill of Materials</h2>

        <div class="bom-grid">
            <div class="bom-card">
                <h4>Core Components</h4>
                <ul>
                    <li>✓ Eaton M65 Supercharger</li>
                    <li>✓ Custom bracket kit (mounting + hardware)</li>
                    <li>✓ Crank pulley / drive pulley</li>
                    <li>✓ Belt system</li>
                    <li>✓ Idler pulleys (2x)</li>
                </ul>
            </div>

            <div class="bom-card">
                <h4>Air & Intake System</h4>
                <ul>
                    <li>✓ Intake piping</li>
                    <li>✓ Charge piping</li>
                    <li>✓ Intercooler (Subaru STI)</li>
                    <li>✓ Silicone couplers & clamps</li>
                </ul>
            </div>

            <div class="bom-card">
                <h4>Monitoring & Control</h4>
                <ul>
                    <li>✓ Adjustable blow-off valve</li>
                    <li>✓ Boost gauge</li>
                    <li>✓ Wideband O2 sensor</li>
                    <li>✓ AFR gauge kit</li>
                </ul>
            </div>
        </div>

        <div style="background: white; padding: 20px; border-radius: 8px; margin-top: 30px; border-left: 4px solid var(--primary);">
            <h4 style="color: var(--primary); margin-bottom: 10px;">⚠️ What You'll Need Separately</h4>
            <p>This kit provides the supercharger mounting solution. You'll also need:</p>
            <ul style="margin-top: 15px; margin-left: 20px;">
                <li><strong>Upgraded fuel injectors</strong> for safe operation</li>
                <li><strong>High-flow fuel pump</strong> to support forced induction</li>
                <li><strong>ECU tuning / calibration</strong> (critical for reliability)</li>
                <li><strong>Colder spark plugs</strong> (recommended)</li>
                <li><strong>Oil catch can</strong> (strongly recommended)</li>
            </ul>
        </div>
    </section>

    <!-- Pricing Section -->
    <section id="pricing">
        <h2>Pricing</h2>
        <div class="price-breakdown">
            <div class="price-item">
                <span>Eaton M65 Supercharger (tested)</span>
                <strong>$650</strong>
            </div>
            <div class="price-item">
                <span>Custom Bracket Kit + Hardware</span>
                <strong>$450</strong>
            </div>
            <div class="price-item">
                <span>Blow-Off / Bypass Valve</span>
                <strong>$90</strong>
            </div>
            <div class="price-item">
                <span>AFR Gauge Kit</span>
                <strong>$120</strong>
            </div>
            <div class="price-item">
                <span>Intercooler (used, Subaru STI)</span>
                <strong>$200</strong>
            </div>
            <div class="price-item">
                <span>Intake Piping & Couplers</span>
                <strong>$180</strong>
            </div>
            <div class="price-item">
                <span>Belt, Pulleys & Components</span>
                <strong>$150</strong>
            </div>
            <div class="price-total">
                Total: $1,840 CAD
            </div>
            <div class="price-note">
                Plus shipping and taxes. Designed for ~3–5 PSI reliable daily use. Works with stock ECU on 91 octane fuel.
            </div>
        </div>
    </section>

    <!-- FAQ Section -->
    <section id="faq" class="faq-section">
        <h2>Frequently Asked Questions</h2>
        <div class="faq-grid">
            <div class="faq-item">
                <h4>How long does installation take?</h4>
                <p>Roughly 1 day if you're ready and have a shop or fabrication experience. Professional installation recommended for best results.</p>
            </div>

            <div class="faq-item">
                <h4>Will this work on my stock Jimny?</h4>
                <p>Yes, it's designed for the Suzuki Jimny M13A (2007+). Your engine will absolutely love the extra torque.</p>
            </div>

            <div class="faq-item">
                <h4>Do I need ECU tuning?</h4>
                <p>YES. Proper tuning is critical for reliability and performance. This kit is designed to work with 91 octane fuel with stock ECU, but professional tuning is strongly recommended.</p>
            </div>

            <div class="faq-item">
                <h4>Can I use a different supercharger?</h4>
                <p>The M65 is the sweet spot for the M13A. It offers the best balance of power and reliability. Other units may require additional fabrication.</p>
            </div>

            <div class="faq-item">
                <h4>How much power are we talking about?</h4>
                <p>Expect significant low-end torque gains—exactly what these rigs need for rock crawling, trails, and daily driving. The M65 provides consistent, usable power.</p>
            </div>

            <div class="faq-item">
                <h4>What's the warranty?</h4>
                <p>The Eaton M65 is a proven OEM unit built to last. Seals and bearings rarely need servicing. Rebuild kits are readily available if needed.</p>
            </div>

            <div class="faq-item">
                <h4>Can I see it installed?</h4>
                <p>Yes! We have photos and videos of the prototype kit on my personal Jimny. Contact us to see the full install gallery.</p>
            </div>

            <div class="faq-item">
                <h4>What if I'm not mechanically inclined?</h4>
                <p>No problem. We can help connect you with shops that specialize in Jimny performance work. Professional installation is always the safest option.</p>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="contact-section">
        <h2 style="color: white;">Ready to Boost Your Jimny?</h2>
        <p style="font-size: 1.1em;">Reach out with questions or to place an order.</p>

        <div class="contact-links">
            <a href="https://www.facebook.com/travis.watkins.940" class="contact-link">💬 Message on Facebook</a>
            <a href="mailto:contact@smalltownboost.com" class="contact-link">📧 Email Us</a>
            <a href="https://www.instagram.com/smalltownboost" class="contact-link">📸 Instagram</a>
        </div>

        <p style="margin-top: 40px; font-size: 0.95em; opacity: 0.8;">
            Located in Alberta, Canada. Ship worldwide. Custom fabrication available for other platforms.
        </p>
    </section>

    <!-- Footer -->
    <footer>
        <p>&copy; 2026 Smalltownboost. All rights reserved.</p>
        <p>Built for Jimny lovers. Trail-proven. Reliable. Simple.</p>
    </footer>
</body>
</html>'''

    return html


def save_website(html_content, output_dir='.tmp/website'):
    """Save generated HTML to file"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    html_file = output_path / 'index.html'
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✓ Product website generated: {html_file}")
    return output_path


def main():
    print("\n" + "="*60)
    print("Product Sales Website Generator")
    print("Jimny M65 Supercharger Kit")
    print("="*60 + "\n")

    print("🔨 Generating product website...")
    html = generate_product_html()

    output_dir = save_website(html)

    print(f"\n✓ Website ready!")
    print(f"📁 Location: {output_dir.absolute()}/index.html")
    print(f"\n📖 Open in browser to view")
    print("\n✨ Features:")
    print("   ✓ Hero section with CTAs")
    print("   ✓ Features grid")
    print("   ✓ Complete BOM")
    print("   ✓ Pricing breakdown")
    print("   ✓ FAQ section")
    print("   ✓ Contact/order links")
    print("   ✓ Mobile responsive")


if __name__ == "__main__":
    main()
