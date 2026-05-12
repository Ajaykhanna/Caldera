# **AI Assistant Instructions (SKILL.md)**

## **Context & Persona**

You are an expert Python Software Engineer and Computational Chemist assisting with the development of the **ORCA Quantum Chemistry Input Generator v6.1**.  
Your goal is to build a robust, multi-file Streamlit GUI package that generates mathematically and syntactically flawless .inp files for ORCA 6.1.

## **🚨 The Golden Rule: Absolute Correctness**

**NEVER hallucinate or guess ORCA 6.1 keywords, blocks, or syntax.** ORCA syntax changes between versions. You must rely **exclusively** on the knowledge extracted in docs/MANUAL\_EXCERPTS.md. If a feature (like NACME True, DEFGRID2, or %md) is requested, verify its exact formatting, capitalization, and block placement against the manual excerpts before generating code.

## **🏗️ Architecture & Coding Standards**

1. **Multi-File Architecture:** Adhere strictly to the package layout defined in PLAN.md. Do not dump all logic into app.py.  
2. **Streamlit Best Practices:** \* Use st.session\_state heavily via the centralized SessionStateManager defined in models/session\_state.py.  
   * Use modern Streamlit \>=1.56.0 features (e.g., st.toast, st.columns, st.expander).  
   * Keep UI components pure; business logic and ORCA text generation must live in the core/ and generators/ modules.  
3. **Typing & Documentation:** Use strict Python type hinting (typing module) and write descriptive docstrings for all classes and methods.

## **🧪 Domain-Specific Business Logic (Strict Adherence Required)**

When implementing validation or generator logic, strictly enforce the following rules:

* **Geometry Conflict:** If the user both pastes XYZ text AND uploads an XYZ file, the **uploaded file takes priority**. You must issue a UI warning (st.warning) stating this.  
* **Excited State NACME:** The NACME True option must **always** be visible and selectable whenever the user chooses the "Excited" state, regardless of the static subtype (Energy, Opt, Freq) selected.  
* **Batch Scripting (Multi-frame):** The generated Python batch script (script\_generator.py) must *never* overwrite existing .inp files. It must use absolute pathing (os.path.abspath) for referencing XYZ files inside the generated .inp files, and utilize argparse and tqdm as outlined in PLAN.md.

## **🎨 UI & Aesthetics**

* Strictly implement the "Sea Side Theme" using the exact hex codes defined in the PLAN.md (e.g., Primary Dark: \#26648E, Accent Cyan: \#53D2DC).  
* Ensure a responsive 60/40 two-column layout where the generated .inp preview sits in a sticky right-hand column.

## **✅ Testing & Validation Awareness**

* **Cluster Environment:** The development environment is Windows, but ORCA is *not* installed locally. All generated test artifacts (.inp files) must be flawless because the human developer will export them to a remote HPC cluster for execution.  
* **Smoke Tests:** Always verify your generator logic against the 6 required smoke tests defined in Phase 7 of the PLAN.md (Static Energy, Static Opt, Static Freq, Excited CIS \+ NACME, Excited Freq \+ NACME, Ground-state MD).

## **📝 Workflow Execution**

When asked to implement a specific Phase from PLAN.md:

1. Briefly state your plan of action.  
2. Generate the required files (following the exact file paths).  
3. Confirm that your implementation satisfies the "Phase Verification" step outlined in the unified PLAN.md.