## Architecture:

- User inputs Vehicle Details 
- Validate inputs
- Feature Engineering on Inputs
- Run XGBoost (Predicted Price, SmartBuy score, SHAP, Depreciation Curve)
- Run Model Market Analysis (clustering and then segment comparison)
- Similar listings scraper
- Collect data and feed to Gemini API
- Feed to Streamlit

smart-buy-classifier/
    -- app.py

    -- tests/
        --validate.py

    -- modules/
        --feature_eng.py
        --run_model.py
        --shap.py
        --depreciation.py
        --find_cluster.py
        --charts.py
        --gemini.py
        --listing_scraper.py

    --data/
        --kmodes.csv
        --seg0.csv
        --seg1.csv
        --seg2.csv
        --seg3,csv
        --data.csv
    
    -- models/
        --xgb.pkl

-- .env
-- .gitignore
-- requirements.txt