import time
import streamlit as st
from streamlit_option_menu import option_menu 
from utils.checker import PasswordAnalyzer
from utils.generator  import PasswordGenerator
import streamlit.components.v1 as components

# Configure page
st.set_page_config(
    page_title="SecurePass Analyzer",
    page_icon="favicon.ico",
    layout="wide"
)

# Initialize components
analyzer = PasswordAnalyzer()
generator = PasswordGenerator()

# Custom CSS
st.markdown("""
<style>
    /* Original custom styles */
    .stProgress > div > div > div > div {
        background-color: #2ECC71;
    }
    .st-bb {
        background-color: transparent;
    }
    .st-at {
        background-color: #2ECC71;
    }
    .st-ae {
        background-color: #F1C40F;
    }
    .st-af {
        background-color: #000 !important;
    }

    /* Keep password & text inputs white with black text */
    input[type="password"], input[type="text"] {
        background-color: #fff !important;
        color: #000 !important;
    }

    /* Eye icon always white, transparent background */
    button[aria-label="Show password"], 
    button[aria-label="Hide password"] {
        background: transparent !important;
    }
    button[aria-label="Show password"] svg,
    button[aria-label="Hide password"] svg {
        color: #fff !important;
    }
</style>
""", unsafe_allow_html=True)

def main():
    with st.sidebar:
        choice = option_menu(
            menu_title="SecurePass",
            options=["Analyzer", "Generator", "Documentation"],
            icons=["shield-check", "key", "book"],
            default_index=0,
            styles={
                "container": {"padding": "5px"},
                "icon": {"color": "#2ECC71", "font-size": "18px"}, 
                "nav-link": {"font-size": "16px", "text-align": "left"},
                "nav-link-selected": {"background-color": "#2ECC71"},
            }
        )

    if choice == "Analyzer":
        st.header("🔍 Password Strength Analyzer")
        with st.form("password_form"):
            col1, col2 = st.columns([3, 1])
            with col1:
                password = st.text_input(
                    "Enter password:", 
                    type="password",
                    placeholder="Enter your password..."
                )
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                analyze_btn = st.form_submit_button("Analyze Security")
            
            if analyze_btn:
                if not password:
                    st.error("Please enter a password to analyze")
                else:
                    with st.spinner("Analyzing security..."):
                        time.sleep(0.5)
                        score, analysis, entropy = analyzer.analyze_password(password)
                        
                        # Visual progress
                        progress = score / 10
                        color = "#E74C3C" if score < 4 else "#F1C40F" if score < 7 else "#2ECC71"
                        
                        with st.container():
                            st.markdown(f"""
                            <div style="padding: 20px; border-radius: 10px; background: rgba(46, 204, 113, 0.1);">
                                <h3 style="color: {color};">Security Score: {score}/10</h3>
                                <div style="height: 10px; background: #eee; border-radius: 5px;">
                                    <div style="width: {progress*100}%; height: 100%; background: {color}; border-radius: 5px;"></div>
                                </div>
                                <p>Entropy: {entropy:.1f} bits</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Detailed analysis
                            st.subheader("🔬 Detailed Analysis")
                            cols = st.columns(4)
                            criteria = {
                                "Length ≥ 8": analysis['length'],
                                "Uppercase": analysis['uppercase'],
                                "Lowercase": analysis['lowercase'],
                                "Digits": analysis['digit'],
                                "Special Chars": analysis['special'],
                                "Uncommon": not analysis['common'],
                                "No Repeats": not analysis['repeats'],
                                "No Sequences": not analysis['sequential']
                            }
                            
                            for (text, status), col in zip(criteria.items(), cols * 2):
                                col.markdown(f"""
                                <div style="margin: 10px 0; padding: 15px; border-radius: 10px; 
                                            background: {'#2ECC7120' if status else '#E74C3C20'}">
                                    <span style="color: {'#2ECC71' if status else '#E74C3C'}">
                                        {'✓' if status else '✗'}
                                    </span> {text}
                                </div>
                                """, unsafe_allow_html=True)
                            
                            # Recommendations
                            st.subheader("📈 Recommendations")
                            if score < 4:
                                st.error("**Immediate Action Required** - This password is extremely vulnerable!")
                                if analysis['common']:
                                    st.error("→ This password is in common breach lists")
                                if not analysis['length']:
                                    st.error("→ Extend password length to at least 12 characters")
                            elif score < 7:
                                st.warning("**Needs Improvement** - Consider these enhancements:")
                                if not analysis['special']:
                                    st.warning("→ Add special characters (!@#$%^&*)")
                                if analysis['sequential']:
                                    st.warning("→ Avoid sequential patterns (abc, 123, etc.)")
                            else:
                                st.success("**Excellent Security!** - This password meets enterprise-grade standards")

    elif choice == "Generator":
        st.header("🔑 Secure Password Generator")
        col1, col2 = st.columns(2)
        with col1:
            length = st.slider("Password Length", 12, 32, 16)
            generate_btn = st.button("Generate Secure Password")
        
        if generate_btn:
            with st.spinner("Generating military-grade password..."):
                time.sleep(0.3)
                password = generator.generate_password(length)
                st.code(password, language="text")
                st.success("Password generated successfully!")
                st.markdown(f"""
                <div style="padding: 15px; background: #2ECC7120; border-radius: 10px;">
                    {password}
                </div>
                """, unsafe_allow_html=True)
                
                # Inject HTML and JavaScript for copy-to-clipboard functionality
                html_code = f"""
                <html>
                  <head>
                    <meta charset="utf-8">
                  </head>
                  <body>
                    <button id="copy-btn" 
                            style="background: #2ECC71; color: white; border: none; padding: 8px 16px; 
                                   border-radius: 5px; margin-top: 10px;">
                        Copy to Clipboard
                    </button>
                    <script>
                      document.getElementById("copy-btn").addEventListener("click", function() {{
                        navigator.clipboard.writeText("{password}").then(function() {{
                          alert("Copied to clipboard!");
                        }}, function(err) {{
                          alert("Failed to copy: " + err);
                        }});
                      }});
                    </script>
                  </body>
                </html>
                """
                components.html(html_code, height=150)

    elif choice == "Documentation":
        st.header("📚 Security Documentation")
        with st.expander("Password Best Practices"):
            st.markdown("""
            - **Minimum 12 Characters**: Longer passwords exponentially increase security
            - **Mix Character Types**: Use upper/lower case, numbers, and symbols
            - **Avoid Patterns**: Sequential numbers/letters reduce security
            - **Unique Passwords**: Never reuse passwords across accounts
            """)
        
        with st.expander("Security Metrics Explained"):
            st.markdown("""
            - **Entropy**: Measures password unpredictability (higher = better)
            - **Common Patterns**: Checks for dictionary words and common sequences
            - **Blacklist Check**: Verifies against 10,000+ breached passwords
            """)

if __name__ == "__main__":
    main()