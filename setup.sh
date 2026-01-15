#!/bin/bash

mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"\"\n\
\n\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = $PORT\n\
\n\
[theme]\n\
primaryColor = '#667eea'\n\
backgroundColor = '#0e1117'\n\
secondaryBackgroundColor = '#262730'\n\
textColor = '#fafafa'\n\
font = 'sans serif'\n\
" > ~/.streamlit/config.toml
