import streamlit as st
import datetime
from research_backend import research_company

# Initialize session state
if 'research_complete' not in st.session_state:
    st.session_state.research_complete = False
if 'research_data' not in st.session_state:
    st.session_state.research_data = ""
if 'company_name' not in st.session_state:
    st.session_state.company_name = ""

# Page configuration
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .research-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .status-box {
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
</style>
""", unsafe_allow_html=True)

# Main Streamlit App
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🔍 AI Research Assistant</h1>
        <p>Comprehensive AI and LLM project research for companies</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Instructions")
        st.markdown("""
        1. Enter a company name in the input field
        2. Click 'Start Research' to begin analysis
        3. View the comprehensive report
        4. Download the results when complete
        
        **What this tool analyzes:**
        - AI/LLM projects and initiatives
        - Technology partnerships
        - Use cases and applications
        - ROI and benefits
        - Risks and challenges
        - Technical architecture
        - Industry comparisons
        """)
        
        st.header("⚙️ Settings")
        if st.button("Clear Cache", help="Clear cached API connections"):
            st.cache_data.clear()
            st.success("Cache cleared!")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Company Research")
        company_name = st.text_input(
            "Enter Company Name:",
            placeholder="e.g., Microsoft, Google, OpenAI...",
            help="Enter the name of the company you want to research"
        )
    
    with col2:
        st.header("Actions")
        if st.button("🚀 Start Research", type="primary", disabled=not company_name.strip()):
            if company_name.strip():
                st.session_state.company_name = company_name.strip()
                st.session_state.research_complete = False
                st.session_state.research_data = ""

                # Step-by-step status and progress
                status_placeholder = st.empty()
                progress_bar = st.progress(0)
                search_queries_placeholder = st.empty()

                def status_callback(msg):
                    status_placeholder.info(msg)

                def progress_callback(val):
                    progress_bar.progress(val)

                def search_callback(queries):
                    search_queries_placeholder.write(f"Search queries: {queries}")

                try:
                    with st.spinner("Researching company... This may take a few minutes."):
                        research_result = research_company(
                            company_name.strip(),
                            progress_callback=progress_callback,
                            status_callback=status_callback,
                            search_callback=search_callback
                        )
                    if research_result:
                        st.session_state.research_data = research_result
                        st.session_state.research_complete = True
                        st.success("Research completed successfully!")
                    else:
                        st.error("Research failed. Please try again.")
                except Exception as e:
                    st.error(str(e))
                finally:
                    progress_bar.empty()
                    status_placeholder.empty()
                    search_queries_placeholder.empty()
    
    # Display results
    if st.session_state.research_complete and st.session_state.research_data:
        st.header(f"📊 Research Results: {st.session_state.company_name}")
        
        # Download button
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_company_name = "".join(c if c.isalnum() else "_" for c in st.session_state.company_name)
            filename = f"{safe_company_name}_AI_Research_Report_{timestamp}.md"
            
            st.download_button(
                label="📥 Download Report (Markdown)",
                data=st.session_state.research_data,
                file_name=filename,
                mime="text/markdown",
                help="Download the complete research report as a Markdown file"
            )
        
        with col2:
            # Convert markdown to plain text for TXT download
            plain_text = st.session_state.research_data
            txt_filename = f"{safe_company_name}_AI_Research_Report_{timestamp}.txt"
            
            st.download_button(
                label="📄 Download Report (Text)",
                data=plain_text,
                file_name=txt_filename,
                mime="text/plain",
                help="Download the complete research report as a plain text file"
            )
        
        # Display the research report
        st.markdown("### Research Report")
        st.markdown(st.session_state.research_data, unsafe_allow_html=True)
        st.text_area("Full Research Report (Plain Text)", st.session_state.research_data, height=800)
        
        # Option to start new research
        if st.button("🔄 Start New Research"):
            st.session_state.research_complete = False
            st.session_state.research_data = ""
            st.session_state.company_name = ""
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>AI Research Assistant - Powered by OpenAI GPT-4 and Tavily Search</p>
        <p>Built with Streamlit 🎈</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
