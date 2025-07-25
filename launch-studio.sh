#!/bin/bash

echo '🚀 Launching Clinical Outreach Agent in LangGraph Studio'
echo '======================================================'

# Check if langgraph-studio is installed
if ! command -v langgraph &> /dev/null; then
echo '📦 Installing LangGraph Studio...'
    pip install langgraph-studio
fi

# Check if .env exists
if [ ! -f .env ]; then
echo '⚠️  .env file not found!'
echo 'Please copy .env.example to .env and set your OpenAI API key'
    exit 1
fi

# Check if OpenAI API key is set
if ! grep -q "OPENAI_API_KEY=sk-" .env; then
echo '⚠️  OpenAI API key not set in .env file'
echo 'Please set OPENAI_API_KEY=your_actual_key in .env'
    exit 1
fi

echo '✅ Environment configured'
echo '🎯 Opening LangGraph Studio...'

# Launch LangGraph Studio
langgraph studio

echo '🎉 LangGraph Studio launched!'
echo '📊 Open your browser to interact with the Clinical Outreach Agent'
