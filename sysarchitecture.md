## Architecture:

- User inputs Vehicle Details 
- Validate inputs
- Feature Engineering on Inputs
- Run XGBoost (Predicted Price, SmartBuy score, SHAP, Depreciation Curve)
- Run Model Market Analysis (clustering and then segment comparison)
- Similar listings scraper
- Collect data and feed to Gemini API
- Feed to Streamlit

---

## File Structure:

smart-buy-classifier/
    -- app.py

    -- tests/
        --validate.py

    -- modules/
        -- schema.py -> data object creation for the Used Car
        --feature_eng.py -> Precprocess user-input vehicle
        --run_model.py -> predict price with XGB
        --shap.py -> SHAP value calculations
        --depreciation.py -> Calculate Depreciation values
        --find_cluster.py -> find relevant cluster in Model Cluster and does Cluster-specific analysis
        --charts.py -> Implement Depreciation Curve Chart and SHAP Plot
        --gemini.py -> Adds AI Market Agent functionality
        --listing_scraper.py
        --streamlit_ui.py

    --data_models/
        --xgb.pkl
        --kmodes.csv
        --seg0.csv
        --seg1.csv
        --seg2.csv
        --seg3,csv
        --data.csv
    
-- .env
-- .gitignore
-- requirements.txt