import time
import streamlit as st
from streamlit_option_menu import option_menu 
from utils.checker import PasswordAnalyzer
from utils.generator import PasswordGenerator
import streamlit.components.v1 as components

# Configure page with different settings
st.set_page_config(
    page_title="PassGuard Pro",
    page_icon="favicon.ico",
    layout="centered"
)

# Initialize components
analyzer = PasswordAnalyzer()
generator = PasswordGenerator()

# New custom CSS with different color scheme
st.markdown("""
<style>
    /* New color scheme - purple and blue */
    .stProgress > div > div > div > div {
        background-color: #6A5ACD;
    }
    .st-bb {
        background-color: transparent;
    }
    .st-at {
        background-color: #4169E1;
    }
    .st-ae {
        background-color: #9370DB;
    }
    .st-af {
        background-color: #000 !important;
    }
            
    /* Main color scheme - purple and blue */
    .stProgress > div > div > div > div {
        background-color: #6A5ACD;
    }
    
    /* Improved sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #F8F9FF !important;
        border-right: 1px solid #E0E0E0;
    }
    
    /* Sidebar text color */
    [data-testid="stSidebar"] .st-emotion-cache-16txtl3 {
        color: #333333 !important;
    }
    
    /* Sidebar menu item styling */
    .st-eb {
        color: #333333 !important;
    }
            
    /* Sidebar selected item */
    .st-c7 {
        background-color: #6A5ACD !important;
        color: white !important;
    }
    
    /* Sidebar hover effect */
    .st-c6:hover {
        background-color: #E6E6FA !important;
    }

    /* Input fields */
    input[type="password"], input[type="text"] {
        background-color: #F8F9FF !important;
        color: #000 !important;
        border: 1px solid #6A5ACD !important;
    }

    /* Eye icon styling */
    button[aria-label="Show password"], 
    button[aria-label="Hide password"] {
        background: transparent !important;
    }
    button[aria-label="Show password"] svg,
    button[aria-label="Hide password"] svg {
        color: #6A5ACD !important;
    }

    /* Custom card styling */
    .custom-card {
        padding: 20px;
        border-radius: 15px;
        background: rgba(106, 90, 205, 0.1);
        border-left: 5px solid #6A5ACD;
        margin-bottom: 20px;
    }

    /* Different hover effects */
    .stButton>button:hover {
        background-color: #6A5ACD !important;
        color: white !important;
        border: 1px solid #6A5ACD !important;
    }
</style>
""", unsafe_allow_html=True)

def main():
    with st.sidebar:
        choice = option_menu(
            menu_title="PassGuard Pro",
            options=["Analyzer", "Generator", "Documentation"],
            icons=["shield-lock", "key-fill", "file-earmark-text"],
            default_index=0,
            styles={
                "container": {
                    "padding": "10px",
                    "background-color": "#F8F9FF",
                    "border-radius": "8px"
                },
                "icon": {
                    "color": "#6A5ACD", 
                    "font-size": "18px"
                }, 
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "8px 0",
                    "color": "#333333",
                    "border-radius": "5px",
                    "padding": "10px"
                },
                "nav-link-selected": {
                    "background-color": "#6A5ACD",
                    "color": "white",
                    "font-weight": "bold",
                    "border-left": "4px solid #4169E1"
                },
            }
        )

    if choice == "Analyzer":
        st.header("🔍 Password Strength Inspector")
        with st.form("password_form"):
            col1, col2 = st.columns([3, 1])
            with col1:
                password = st.text_input(
                    "Enter password to analyze:", 
                    type="password",
                    placeholder="Type your password here...",
                    help="We never store your passwords"
                )
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                analyze_btn = st.form_submit_button("Evaluate Security")
            
            if analyze_btn:
                if not password:
                    st.error("Please enter a password to analyze")
                else:
                    with st.spinner("Conducting security analysis..."):
                        time.sleep(0.5)
                        score, analysis, entropy = analyzer.analyze_password(password)
                        
                        # Visual progress with new colors
                        progress = score / 10
                        color = "#FF6347" if score < 4 else "#FFA500" if score < 7 else "#4169E1"
                        
                        with st.container():
                            st.markdown(f"""
                            <div class="custom-card">
                                <h3 style="color: {color};">Security Rating: {score}/10</h3>
                                <div style="height: 10px; background: #eee; border-radius: 5px; margin: 10px 0;">
                                    <div style="width: {progress*100}%; height: 100%; background: {color}; border-radius: 5px;"></div>
                                </div>
                                <p><strong>Entropy:</strong> {entropy:.1f} bits (higher is better)</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Detailed analysis with new layout
                            st.subheader("🔍 Detailed Inspection")
                            cols = st.columns(2)
                            criteria = {
                                "Length ≥ 8": analysis['length'],
                                "Uppercase Letters": analysis['uppercase'],
                                "Lowercase Letters": analysis['lowercase'],
                                "Numbers": analysis['digit'],
                                "Special Characters": analysis['special'],
                                "Not Common": not analysis['common'],
                                "No Repeated Chars": not analysis['repeats'],
                                "No Sequential Patterns": not analysis['sequential']
                            }
                            
                            for (text, status), col in zip(criteria.items(), cols * 4):
                                col.markdown(f"""
                                <div style="margin: 5px 0; padding: 10px; border-radius: 8px; 
                                            background: {'#4169E120' if status else '#FF634720'}">
                                    <span style="color: {'#4169E1' if status else '#FF6347'}">
                                        {'✓' if status else '✗'}
                                    </span> {text}
                                </div>
                                """, unsafe_allow_html=True)
                            
                            # Recommendations with different styling
                            st.subheader("💡 Security Recommendations")
                            if score < 4:
                                st.error("**Critical Risk** - This password is highly vulnerable to attacks!")
                                if analysis['common']:
                                    st.error("🚨 This password appears in known breach databases")
                                if not analysis['length']:
                                    st.error("🔒 Increase length to at least 12 characters")
                            elif score < 7:
                                st.warning("**Moderate Security** - Consider these improvements:")
                                if not analysis['special']:
                                    st.warning("✨ Add special characters (!@#$%^&*)")
                                if analysis['sequential']:
                                    st.warning("🔢 Avoid sequential patterns (abc, 123, qwerty)")
                            else:
                                st.success("**Excellent Security** - This password meets high security standards")

    elif choice == "Generator":
        st.header("🔐 Smart Password Creator")
        col1, col2 = st.columns([3, 2])
        with col1:
            length = st.slider("Select Password Length", 12, 32, 16, help="Longer passwords are more secure")
            include_symbols = st.checkbox("Include Special Symbols", True)
            generate_btn = st.button("Generate Strong Password", type="primary")
        
        if generate_btn:
            with st.spinner("Creating high-entropy password..."):
                time.sleep(0.3)
                password = generator.generate_password(length)
                
                st.markdown("""
                <div style="margin: 20px 0; padding: 15px; background: #F8F9FF; 
                            border-radius: 10px; border-left: 5px solid #6A5ACD;">
                    <h4 style="color: #6A5ACD; margin: 0;">Your Generated Password:</h4>
                    <p style="font-family: monospace; font-size: 18px; margin: 10px 0;">{password}</p>
                </div>
                """.format(password=password), unsafe_allow_html=True)
                
                # Copy to clipboard functionality with different styling
                html_code = f"""
                <html>
                  <head>
                    <meta charset="utf-8">
                  </head>
                  <body>
                    <button id="copy-btn" 
                            style="background: #6A5ACD; color: white; border: none; padding: 8px 16px; 
                                   border-radius: 5px; margin-top: 10px; cursor: pointer;
                                   transition: all 0.3s ease;">
                        📋 Copy Password
                    </button>
                    <script>
                      document.getElementById("copy-btn").addEventListener("click", function() {{
                        navigator.clipboard.writeText("{password}").then(function() {{
                          this.textContent = "Copied!";
                          this.style.background = "#4169E1";
                          setTimeout(() => {{
                            this.textContent = "📋 Copy Password";
                            this.style.background = "#6A5ACD";
                          }}, 2000);
                        }}.bind(this), function(err) {{
                          alert("Failed to copy: " + err);
                        }});
                      }});
                    </script>
                  </body>
                </html>
                """
                components.html(html_code, height=70)

    elif choice == "Documentation":
        st.header("📖 Security Knowledge Base")
        with st.expander("🔐 Password Creation Guidelines", expanded=True):
            st.markdown("""
            ### Creating Strong Passwords
            
            - **Length Matters**: Aim for at least 12-16 characters
            - **Diversity is Key**: Combine letters (upper and lower case), numbers, and symbols
            - **Avoid Predictability**: Steer clear of common words, phrases, or patterns
            - **Uniqueness**: Never reuse passwords across different accounts
            - **Consider Passphrases**: String of random words can be both strong and memorable
            """)
        
        with st.expander("📊 Understanding Security Metrics"):
            st.markdown("""
            ### How We Evaluate Passwords
            
            - **Entropy Score**: Measures the randomness and unpredictability
            - **Pattern Detection**: Identifies common sequences or keyboard patterns
            - **Breach Database Check**: Compares against known compromised passwords
            - **Character Diversity**: Evaluates use of different character types
            """)
        
        with st.expander("🛡️ Additional Security Tips"):
            st.markdown("""
            - Use a reputable password manager to store your passwords
            - Enable two-factor authentication wherever possible
            - Regularly update important passwords (every 3-6 months)
            - Be cautious of phishing attempts asking for your credentials
            """)

if __name__ == "__main__":
    main()