# **PLAN.md \- ORCA GUI Interface Blueprint (UNIFIED)**

## **Project Overview**

**Project Name:** ORCA Quantum Chemistry Input Generator  
**Version:** 6.1  
**Framework:** Python \+ Streamlit 1.56.0 \+ HTML \+ CSS  
**Architecture:** Multi-file Python Package  
**Developer:** Ajay Khanna, LANL  
**Date:** May-01-2026  
**Target:** Modular, maintainable Python package with Streamlit frontend.  
**Core Mandate:** Absolute correctness via strict parsing of the ORCA 6.1 manual to extract verified syntax into docs/MANUAL\_EXCERPTS.md.

## **📐 Design Specifications**

### **Color Palette (Sea Side Theme)**

PRIMARY\_DARK \= "\#26648E"      \# Deep Ocean Blue \- Headers, primary buttons  
PRIMARY\_MEDIUM \= "\#4F8FC0"    \# Ocean Blue \- Secondary elements, borders  
ACCENT\_CYAN \= "\#53D2DC"       \# Cyan \- Highlights, active states, links  
ACCENT\_WARM \= "\#FFE3B3"       \# Warm Sand \- Warnings, info boxes, hover states  
BACKGROUND \= "\#F8FAFB"        \# Light background  
TEXT\_DARK \= "\#1A1A1A"         \# Primary text  
TEXT\_LIGHT \= "\#6B7280"        \# Secondary text  
SUCCESS \= "\#10B981"           \# Success messages  
ERROR \= "\#EF4444"             \# Error messages  
WARNING \= "\#F59E0B"           \# Warning messages

### **Layout Structure**

┌─────────────────────────────────────────────────────────────────────────┐  
│  \[🔬 LOGO\]  ORCA Input File Generator v6.1           \[💾 Save\] \[📂 Load\] │  
├──────────────────────────────┬──────────────────────────────────────────┤  
│ LEFT COLUMN (60%)            │ RIGHT COLUMN (40% \- Sticky)              │  
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━ │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │  
│                              │                                          │  
│ \[Scrollable Content Area\]    │ 📄 Generated Input File                  │  
│                              │ ┌──────────────────────────────────────┐ │  
│ ┌──────────────────────────┐ │ │ \! B3LYP 6-31G(d) OPT                │ │  
│ │ 📋 Preset Templates       │ │ │                                     │ │  
│ │ \[Dropdown: Select...\]     │ │ │ %pal nprocs 4 end                   │ │  
│ └──────────────────────────┘ │ │ %maxcore 1000                       │ │  
│                              │ │                                     │ │  
│ ┌──────────────────────────┐ │ │ \* xyzfile 0 1 geometry.xyz          │ │  
│ │ 🔄 Batch Processing       │ │ │                                     │ │  
│ │ \[▼ Expand/Collapse\]       │ │ └──────────────────────────────────────┘ │  
│ └──────────────────────────┘ │                                          │  
│                              │ Filename: \[frame\_1.inp    \]              │  
│ ┌──────────────────────────┐ │                                          │  
│ │ 🧪 Calculation Type       │ │ \[📋 Copy to Clipboard\]                   │  
│ │ ○ Static  ○ Dynamics      │ │ \[💾 Download .inp\]                       │  
│ └──────────────────────────┘ │                                          │  
│                              │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │  
│ ┌──────────────────────────┐ │ 📊 Validation Status                     │  
│ │ 🎯 State Selection        │ │ ✅ All checks passed                     │  
│ │ ○ Ground  ○ Excited       │ │                                          │  
│ └──────────────────────────┘ │                                          │  
│                              │                                          │  
│ \[Dynamic sections based on   │                                          │  
│  calculation type selected\]  │                                          │  
│                              │                                          │  
│ ┌──────────────────────────┐ │                                          │  
│ │ 📐 Geometry Input         │ │                                          │  
│ └──────────────────────────┘ │                                          │  
│                              │                                          │  
│ ┌──────────────────────────┐ │                                          │  
│ │ ⚙️ Advanced Options       │ │                                          │  
│ │ \[▼ Expand/Collapse\]       │ │                                          │  
│ └──────────────────────────┘ │                                          │  
│                              │                                          │  
│ \[🚀 Generate Input File\]     │                                          │  
│                              │                                          │  
└──────────────────────────────┴──────────────────────────────────────────┘  
│ 👨‍💻 Developer: Ajay Khanna | LANL | May 2026                              │  
└─────────────────────────────────────────────────────────────────────────┘

## **🏗️ Package Architecture & File Structure**

### **Complete Package Structure**

orca\_gui/  
├── README.md                          \# User documentation  
├── PLAN.md                            \# This file \- blueprint  
├── LICENSE                            \# License file  
├── requirements.txt                   \# Python dependencies  
├── setup.py                           \# Package installation  
├── .gitignore                         \# Git ignore file  
│  
├── .streamlit/                        \# Streamlit configuration  
│   └── config.toml                    \# Theme and server settings  
│  
├── orca\_gui/                          \# Main package directory  
│   ├── \_\_init\_\_.py                      
│   ├── \_\_version\_\_.py                   
│   ├── app.py                         \# Main Streamlit application entry point  
│   │  
│   ├── config/                          
│   │   ├── \_\_init\_\_.py  
│   │   ├── constants.py               \# Color palette, defaults, ORCA keywords  
│   │   ├── settings.py                  
│   │   └── orca\_keywords.py           \# ORCA-specific keyword definitions verified by manual  
│   │  
│   ├── models/                          
│   │   ├── \_\_init\_\_.py  
│   │   ├── calculation.py               
│   │   ├── geometry.py                  
│   │   ├── method.py                    
│   │   └── session\_state.py           \# Session state manager (includes batch params)  
│   │  
│   ├── core/                            
│   │   ├── \_\_init\_\_.py  
│   │   ├── input\_generator.py           
│   │   ├── validator.py               \# Validation \+ geometry priority/NACME rules  
│   │   ├── geometry\_parser.py           
│   │   └── batch\_processor.py           
│   │  
│   ├── generators/                      
│   │   ├── \_\_init\_\_.py  
│   │   ├── ground\_state.py              
│   │   ├── excited\_state.py             
│   │   ├── dynamics.py                  
│   │   ├── zip\_generator.py             
│   │   └── script\_generator.py        \# Python batch script generator with argparse & TQDM  
│   │  
│   ├── ui/                              
│   │   ├── \_\_init\_\_.py  
│   │   ├── components/                \# Reusable UI components  
│   │   │   ├── \_\_init\_\_.py  
│   │   │   ├── header.py                
│   │   │   ├── footer.py                
│   │   │   ├── preset\_templates.py      
│   │   │   ├── batch\_settings.py        
│   │   │   ├── calculation\_type.py      
│   │   │   ├── state\_selector.py        
│   │   │   ├── level\_of\_theory.py       
│   │   │   ├── basis\_set.py             
│   │   │   ├── scf\_settings.py          
│   │   │   ├── grid\_settings.py         
│   │   │   ├── geometry\_input.py        
│   │   │   ├── advanced\_options.py      
│   │   │   ├── md\_parameters.py         
│   │   │   ├── output\_config.py         
│   │   │   └── preview\_panel.py         
│   │   │  
│   │   ├── layouts/                     
│   │   │   ├── \_\_init\_\_.py  
│   │   │   ├── main\_layout.py           
│   │   │   ├── static\_layout.py         
│   │   │   └── dynamics\_layout.py       
│   │   │  
│   │   └── styles/                      
│   │       ├── \_\_init\_\_.py  
│   │       ├── custom\_css.py            
│   │       └── theme.py                 
│   │  
│   ├── utils/                           
│   │   ├── \_\_init\_\_.py  
│   │   ├── file\_utils.py                
│   │   ├── path\_utils.py                
│   │   ├── validation\_utils.py          
│   │   ├── clipboard\_utils.py           
│   │   └── session\_utils.py             
│   │  
│   └── templates/                     \# 5 Explicit Presets required  
│       ├── \_\_init\_\_.py  
│       ├── template\_loader.py           
│       ├── preset\_static\_energy.json  
│       ├── preset\_opt.json  
│       ├── preset\_freq.json  
│       ├── preset\_cis\_nacme.json  
│       └── preset\_ground\_md.json  
│  
├── scripts/  
│   └── generate\_manual\_excerpts.py    \# Required Phase 0 ORCA Manual parsing logic  
│  
├── docs/                                
│   ├── user\_guide.md  
│   ├── MANUAL\_EXCERPTS.md             \# Auto-generated single source of truth for syntax  
│   └── ORCA\_manual\_6.1.pdf              
│  
├── examples/                            
│   └── single\_files/  
│  
└── tests/                               
    ├── \_\_init\_\_.py  
    ├── conftest.py                      
    ├── test\_validators.py  
    ├── test\_generators.py  
    ├── test\_workflows.py  
    ├── expected\_features.md           \# Required ORCA output keywords  
    └── golden/                        \# Golden generated test artifacts

## **📦 Module Specifications**

### **1\. Models Module (orca\_gui/models/)**

#### **session\_state.py (Snippet updating Batch variables)**

from dataclasses import dataclass, asdict  
from typing import Any, Dict, Optional

@dataclass  
class SessionState:  
    \# ... previous fields ...  
      
    \# Batch Processing (Updated with CLI explicit arguments)  
    batch\_enabled: bool \= False  
    batch\_start\_frame: int \= 1  
    batch\_end\_frame: int \= 1000  
    batch\_step\_frame: int \= 1  
    batch\_output\_type: str \= 'script' \# default to recommended script mode  
    batch\_base\_dir: str \= ''  
    batch\_xyz\_prefix: str \= 'frame\_'  
    batch\_subdir\_pattern: str \= 'frame\_{}' \# Allows configurable folder naming  
    batch\_filename\_prefix: str \= 'frame\_'  
      
    \# ... rest of fields ...

### **2\. Core Module (orca\_gui/core/)**

#### **validator.py (Snippet updating strict logic rules)**

"""  
Comprehensive validation including strict geometry & NACME rules.  
"""  
class ORCAValidator:  
    \# ... setup ...

    def validate\_geometry(self):  
        """Validate geometry input with priority rules"""  
        if self.state.geometry\_xyz\_file and self.state.geometry\_xyz\_text:  
            self.result.add\_warning(  
                "Both uploaded file and pasted text provided. Prioritizing the uploaded XYZ file."  
            )  
          
        \# ... standard validation ...

    def validate\_excited\_state(self):  
        """Validate excited state parameters (NACME rule)"""  
        if self.state.state\_type \!= 'excited':  
            return  
              
        \# ... standard root checks ...  
          
        \# NACME validation \- Show whenever excited state is selected  
        if self.state.excited\_nacme:  
            \# Note: We rely on docs/MANUAL\_EXCERPTS.md to define if NACME is explicitly   
            \# forbidden for certain static types. By default, GUI allows it per requirements.  
            pass

### **3\. Generators Module (orca\_gui/generators/)**

#### **script\_generator.py**

"""  
Python batch script generator for multi-frame generation.  
"""  
from orca\_gui.models.session\_state import SessionState

class BatchScriptGenerator:  
    """Generates a standalone robust Python script for batch ORCA inputs"""  
      
    def \_\_init\_\_(self, state: SessionState):  
        self.state \= state

    def generate(self) \-\> str:  
        """Generates script with argparse, TQDM, and absolute pathing."""  
          
        script \= f'''\#\!/usr/bin/env python3  
"""  
Generated Batch ORCA Input Creator.  
"""  
import os  
import argparse  
from tqdm import tqdm

def main():  
    parser \= argparse.ArgumentParser(description="Batch generate ORCA inputs.")  
    parser.add\_argument("--base\_dir", required=True, help="Base directory containing XYZ frames")  
    parser.add\_argument("--xyz\_prefix", default="{self.state.batch\_xyz\_prefix}", help="Prefix for xyz files")  
    parser.add\_argument("--start\_frame", type=int, default={self.state.batch\_start\_frame})  
    parser.add\_argument("--end\_frame", type=int, default={self.state.batch\_end\_frame})  
    parser.add\_argument("--step\_frame", type=int, default={self.state.batch\_step\_frame})  
    parser.add\_argument("--output\_prefix", default="{self.state.batch\_filename\_prefix}")  
    parser.add\_argument("--subdir\_pattern", default="{self.state.batch\_subdir\_pattern}")  
      
    args \= parser.parse\_args()  
      
    generated \= 0  
    skipped \= 0  
    failures \= 0  
      
    for i in tqdm(range(args.start\_frame, args.end\_frame \+ 1, args.step\_frame)):  
        subdir \= os.path.join(args.base\_dir, args.subdir\_pattern.format(i))  
        xyz\_file \= os.path.join(subdir, f"{{args.xyz\_prefix}}{{i}}.xyz")  
        inp\_file \= os.path.join(subdir, f"{{args.output\_prefix}}{{i}}.inp")  
          
        if not os.path.exists(xyz\_file):  
            print(f"Warning: {{xyz\_file}} not found, skipping...")  
            failures \+= 1  
            continue  
              
        if os.path.exists(inp\_file):  
            print(f"Warning: {{inp\_file}} already exists, skipping...")  
            skipped \+= 1  
            continue  
              
        try:  
            \# Generate input utilizing absolute paths: os.path.abspath(xyz\_file)  
            inp\_content \= generate\_input\_content(os.path.abspath(xyz\_file))  
            with open(inp\_file, 'w') as f:  
                f.write(inp\_content)  
            generated \+= 1  
        except Exception as e:  
            print(f"Failed on frame {{i}}: {{e}}")  
            failures \+= 1  
              
    print(f"\\\\nSummary: {{generated}} Generated, {{skipped}} Skipped, {{failures}} Failures.")

def generate\_input\_content(abs\_xyz\_path):  
    \# Template dynamically populated by the main GUI  
    return """{self.\_get\_base\_template\_with\_placeholder()}""".replace("{XYZ\_PATH}", abs\_xyz\_path)

if \_\_name\_\_ \== "\_\_main\_\_":  
    main()  
'''  
        return script

## **🎯 Implementation Phases**

### **Phase 0: Manual Parsing & Correctness Strategy**

* \[ \] Create scripts/generate\_manual\_excerpts.py.  
* \[ \] Extract exact syntax and block logic from ORCA 6.1 manual to docs/MANUAL\_EXCERPTS.md.  
* \[ \] Document strict placement of NACME True, DEFGRID2, CPCM, and MD blocks.  
* \[ \] **Phase Verification:** Verify that manual excerpts are correctly extracted, formatted, and working as expected against the actual manual specs.

### **Phase 1: Project Setup & Core Infrastructure**

* \[ \] Create package structure and all directories.  
* \[ \] Set up setup.py, requirements.txt.  
* \[ \] Implement configuration (constants.py, orca\_keywords.py verifying against excerpts).  
* \[ \] Implement data models (session\_state.py).  
* \[ \] **Phase Verification:** Verify that project structure is correctly instantiated and all configurations load appropriately as expected.

### **Phase 2: Core Logic Implementation**

* \[ \] Implement geometry parser & validator (incorporating priority rules).  
* \[ \] Implement base input generator.  
* \[ \] Unit tests for core modules.  
* \[ \] **Phase Verification:** Verify that geometry parsing and validation rules are triggering correctly and working as expected.

### **Phase 3: UI Components \- Basic**

* \[ \] Implement main layout and color palette definitions.  
* \[ \] Implement 5 preset templates based on requirements.  
* \[ \] Implement geometry input component with text/upload conflict handling.  
* \[ \] **Phase Verification:** Verify that Streamlit UI renders perfectly and state binds to components correctly as expected.

### **Phase 4: Advanced Static Features**

* \[ \] Implement SCF and grid settings (IntAccXC/GridXC manual overrides).  
* \[ \] Implement excited state logic ensuring NACME displays independent of static subtype.  
* \[ \] Complete ground/excited state generators.  
* \[ \] **Phase Verification:** Verify all static features output properly formatted blocks and interact correctly as expected.

### **Phase 5: Dynamics Implementation**

* \[ \] Implement MD parameters (Ground state only initially).  
* \[ \] Implement dynamics generator (generators/dynamics.py).  
* \[ \] **Phase Verification:** Verify that MD outputs correctly assemble all required components and function as expected.

### **Phase 6: Batch Processing**

* \[ \] Implement batch settings component.  
* \[ \] Implement robust Python script generator (generators/script\_generator.py) with Argparse/TQDM.  
* \[ \] Testing absolute path resolution logic.  
* \[ \] **Phase Verification:** Verify the Python script generator outputs syntactically valid code and absolute pathing works seamlessly as expected.

### **Phase 7: Polish & Strict Testing**

* \[ \] **Execution of 6 specific smoke tests** (outputs to tests/golden/):  
  1. Static Energy (ground)  
  2. Static Opt (ground)  
  3. Static Freq (ground)  
  4. Excited state CIS energy \+ NACME True  
  5. Excited state with Frequency subtype \+ NACME option  
  6. Ground-state MD template smoke test  
* \[ \] **Cluster Testing Workflow**:  
  * AI will provide the specific test scripts and inputs to run.  
  * *Note:* GUI development is occurring on a Windows platform where ORCA is **not** installed.  
  * The completed package will be exported to a cluster where ORCA is installed.  
  * The user will execute the tests on the cluster and provide the outputs back to the AI for verification and refinement.  
* \[ \] UI/UX refinement and responsiveness check.  
* \[ \] **Phase Verification:** Verify that generated outputs pass execution on the cluster and match intended structures correctly.

### **Phase 8: Final Validation & Deployment**

* \[ \] Full test suite execution against expected\_features.md.  
* \[ \] Final ORCA manual compliance check.  
* \[ \] Deployment preparation.  
* \[ \] **Final Blueprint Verification:** Perform a comprehensive, blueprint-oriented check for all phases to ensure the final product perfectly aligns with this entire PLAN.md document, addressing any gaps before completion.

## **📚 Setup and Installation**

### **setup.py**

from setuptools import setup, find\_packages

setup(  
    name="orca-gui",  
    version="6.1.0",  
    author="Ajay Khanna",  
    description="GUI interface for generating ORCA quantum chemistry input files",  
    packages=find\_packages(),  
    python\_requires="\>=3.8",  
    install\_requires=open("requirements.txt").read().splitlines(),  
    include\_package\_data=True,  
    entry\_points={  
        "console\_scripts": \[  
            "orca-gui=orca\_gui.app:main",  
        \],  
    },  
)

