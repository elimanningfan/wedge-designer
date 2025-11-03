#!/bin/bash
# Launch Streamlit web interface on port 8000

echo "🏌️ Starting Parametric Golf Wedge Designer Web Interface..."
echo "Opening at http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py --server.port 8000
