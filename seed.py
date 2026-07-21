from database import engine, Base, SessionLocal, Category, Product

# 1. Wipe the old database clean so the new technical columns are recognized
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # 2. Re-create the specific scientific categories
    cat1 = Category(name="Cellular Assays")
    cat2 = Category(name="Microscopy")
    cat3 = Category(name="Mycoplasma")
    
    db.add_all([cat1, cat2, cat3])
    db.commit() 

    # --- Rich Data Extraction from the MaRK Technical Datasheet ---
    mark_desc = (
        "Mycoplasma Removal Kit (MaRK) is a specialized reagent designed for the highly effective "
        "elimination of mycoplasma contamination in cell cultures, whether mild or heavy. Sterile-filtered "
        "and cell culture-tested, it targets specific biological functions in mycoplasma without affecting "
        "mammalian cells, allowing you to preserve the structural integrity of your cell lines."
    )
    
    mark_protocol = """
        <h4 style="margin-bottom: 8px; color: var(--dark-slate);">1. Prepare Cells</h4>
        <ul style="margin-left: 20px; margin-bottom: 15px; line-height: 1.6;">
            <li>Remove the contaminated medium from the culture.</li>
            <li>Rinse cells twice with phosphate-buffered saline (PBS) to remove residual surface contaminants.</li>
        </ul>
        
        <h4 style="margin-bottom: 8px; color: var(--dark-slate);">2. Treatment Setup</h4>
        <ul style="margin-left: 20px; margin-bottom: 15px; line-height: 1.6;">
            <li>Split an actively dividing culture into fresh medium containing MaRK at a baseline concentration of 1 μl/ml of media.</li>
            <li><em>Note:</em> For sensitive lines or variant loads, test scaling options between 0.6–1.2 μl/ml to isolate optimal tolerability.</li>
            <li>Ensure cells are in the exponential growth phase before treatment by seeding at an appropriate dilution.</li>
        </ul>
        
        <h4 style="margin-bottom: 8px; color: var(--dark-slate);">3. Maintenance & Verification</h4>
        <ul style="margin-left: 20px; margin-bottom: 15px; line-height: 1.6;">
            <li>Every 3-4 days, passage cells and/or replace the medium with freshly prepared medium containing MaRK.</li>
            <li>Continue this clear regimen for two weeks to ensure absolute, long-term elimination.</li>
            <li>Confirm complete mycoplasma clearance using DAPI staining, PCR, or cell-based colorimetric assays.</li>
        </ul>
    """
    
    mark_specs = """
        <div style="line-height: 1.8;">
            <p style="margin-bottom: 15px;"><strong>Dual-Action Inhibitor Core:</strong> Features a dual composition including a <em>Protein Synthesis Inhibitor</em> to disrupt protein production and a <em>DNA Gyrase Inhibitor</em> to block localized bacterial replication.</p>
            <ul style="margin-left: 20px; margin-bottom: 15px;">
                <li><strong>Storage Temp:</strong> 4°C for up to 1 month, or long-term storage at -20°C (18 months from manufacturing).</li>
                <li><strong>Broad-Spectrum Efficacy:</strong> Validated active against the main species responsible for 95% of cell culture contaminations, including <em>M. arginini, M. fermentans, M. hyorhinis, M. orale,</em> and <em>A. laidlawii</em>.</li>
                <li><strong>Tested & Certified Lines:</strong> MCF10A, MCF7, HEK293T, HEK293, C127I, Neuro2a, and HeLa.</li>
                <li><strong>Package Configuration:</strong> Supplied at 10 mg/ml in 3 premium amber-colored tubes with a final total volume of 1ml.</li>
                <li><strong>Production Profile:</strong> Premium B2B scientific design, Made in India.</li>
            </ul>
        </div>
    """

    # 3. Add all products into the array matrix
    products = [
        # --- CATEGORY 1: CELLULAR ASSAYS ---
        
        
        Product(
    name="DCFDA based ROS Detection Kit", 
    price=12500.00, 
    category_id=cat1.id,
    description="Fluorometric assay for the detection of reactive oxygen species (ROS) in live cells.",
    images="Assets/dcfda/WT 48H woC ben-dcfda n7_Series002 Snapshot1_ch00.jpg",
    image_captions="Amber tubes ensure protection for light-sensitive dyes,Assay results demonstrating cell viability over 48 hours,Epifluorescence microscopy overlaid with Hoechst nuclear stain",
    specs_html="""
        <h3 style="margin-bottom: 10px; color: var(--dark-slate);">Product Overview</h3>
        <p style="margin-bottom: 15px;">This kit utilizes the cell-permeable fluorogenic probe 2',7'-dichlorofluorescin diacetate (DCFDA) to reliably measure hydroxyl, peroxyl, and other reactive oxygen species (ROS) activity within live cells.</p>
        <ul style="margin-left: 20px; margin-bottom: 20px;">
            <li><strong>Detection Method:</strong> Fluorescence (Ex/Em = 485/530 nm)</li>
            <li><strong>Sample Type:</strong> Adherent and suspension living cells</li>
            <li><strong>Assay Time:</strong> ~45 minutes (staining) + incubation</li>
        </ul>
    """,
    protocol_html="""
        <h4 style="margin-bottom: 5px; color: var(--dark-slate);">1. Cell Seeding & Treatment</h4>
        <ul style="margin-left: 20px; margin-bottom: 15px;">
            <li>Seed 1-2 × 10⁵ cells/well in a 24-well plate; incubate overnight.</li>
            <li>Replace medium with fresh DMEM containing either 100 µM ferrous sulfate (FS), test compounds, or vehicle control.</li>
            <li>Incubate for 24 hours at 37 °C.</li>
        </ul>

        <h4 style="margin-bottom: 5px; color: var(--dark-slate);">2. Staining Procedure</h4>
        <ol style="margin-left: 20px; margin-bottom: 15px;">
            <li>Dilute 4.1 mM DCFDA stock to a 10 µM working solution in pre-warmed DMEM.</li>
            <li>Wash cells, add 500 µL working solution, and incubate at 37 °C for 30 minutes in the dark.</li>
            <li>Wash once with DMEM and twice with 1× PBS. Add 500 µL PBS for imaging.</li>
        </ol>

        <h4 style="margin-bottom: 5px; color: var(--dark-slate);">3. Measurement & Analysis</h4>
        <ul style="margin-left: 20px; margin-bottom: 15px;">
            <li><strong>Imaging:</strong> Use GFP filter (Ex: 485 nm, Em: 530 nm).</li>
            <li><strong>Lysis:</strong> Add 200 µL lysis buffer, incubate on ice for 5 min, centrifuge at 21,000 × g for 10 min at 4 °C.</li>
            <li><strong>Quantification:</strong> Measure fluorescence at 485/530 nm and normalize to total protein via Bradford assay.</li>
        </ul>
    """,
    support_html="""
        <h4 style="margin-bottom: 5px; color: var(--dark-slate);">Troubleshooting</h4>
        <p style="margin-bottom: 15px;"><strong>High Background:</strong> DCFDA is light-sensitive; ensure all staining and incubation steps are performed in the dark.</p>
        <p><strong>Normalization:</strong> Ensure consistent protein quantification using the Bradford assay to normalize fluorescence intensity relative to untreated controls for accurate data representation.</p>
    """,
    download_link="/downloads/dcfda-protocol.pdf"
),
        Product(
            name="Calcein AM", 
            price=180.00, 
            category_id=cat1.id,
            description="Reliable and efficient live-cell viability detection suitable for drug screening and toxicity studies.",
            images = "Assets/calcein/C2-CalceinAM MCF10CA1a.lif - 2uM.jpg",
            image_captions="Amber tubes ensure protection for light-sensitive dyes,Assay results demonstrating cell viability over 48 hours,Epifluorescence microscopy overlaid with Hoechst nuclear stain",
            specs_html="""
                <h3 style="margin-bottom: 10px; color: var(--dark-slate);">Product Overview</h3>
                <p style="margin-bottom: 15px;">This assay utilizes a cell-permeable fluorogenic dye that is converted by intracellular esterases into highly fluorescent calcein within live cells, providing a robust, direct indicator of cell viability.</p>
                <ul style="margin-left: 20px; margin-bottom: 20px;">
                    <li><strong>Excitation / Emission:</strong> 490 nm / 525 nm</li>
                    <li><strong>Recommended Working Concentration:</strong> 0.5 µM</li>
                    <li><strong>Applications:</strong> Microplate reader assays and Epifluorescence microscopy</li>
                </ul>
            """,
            protocol_html="""
                <h4 style="margin-bottom: 5px; color: var(--dark-slate);">1. Reagent Preparation</h4>
                <ul style="margin-left: 20px; margin-bottom: 15px;">
                    <li><strong>Stock Solution (1 mM):</strong> Reconstitute the 50 µg vial with 50 µL Dimethyl sulfoxide (DMSO). Mix gently until completely dissolved. Aliquot if necessary and store at −20°C protected from light. Avoid repeated freeze–thaw cycles.</li>
                    <li><strong>Working Solution (0.5 µM):</strong> Dilute 1 µL of 1 mM stock into 1999 µL assay buffer, PBS, or serum-free culture medium immediately before use. Protect from light.</li>
                </ul>

                <h4 style="margin-bottom: 5px; color: var(--dark-slate);">2. 96-Well Plate Fluorescence Assay</h4>
                <ol style="margin-left: 20px; margin-bottom: 15px;">
                    <li><strong>Cell Seeding:</strong> Seed cells at densities of 1 × 10³ – 5 × 10⁵ cells/mL (100 µL per well). Incubate overnight for adherent cell lines to attach.</li>
                    <li><strong>Dye Loading:</strong> Remove culture medium if required. Add 100 µL fresh assay buffer, then add the working solution to achieve a final well concentration of 0.5 µM.</li>
                    <li><strong>Incubation:</strong> Incubate the plate at 37°C for 30 minutes in the dark. <em>(Typical optimal range: 20 minutes to 1 hour).</em></li>
                    <li><strong>Washing:</strong> Remove dye-containing buffer. Wash cells 1–2 times with indicator-free assay buffer to remove excess probe.</li>
                    <li><strong>Measurement:</strong> Record fluorescence intensity using a microplate reader (Excitation: 490 nm | Emission: 525 nm | Cutoff: 515 nm).</li>
                </ol>
            """,
            support_html="""
                <h4 style="margin-bottom: 5px; color: var(--dark-slate);">Notes & Optimization</h4>
                <ul style="margin-left: 20px; margin-bottom: 15px;">
                    <li><strong>Background Interference:</strong> Phenol red and serum esterases in standard culture media may contribute to background fluorescence. Using clear, serum-free buffers is highly recommended during measurement.</li>
                    <li><strong>Protocol Adjustments:</strong> Optimal incubation time varies heavily depending on cell type and density. Note that lower incubation temperatures may reduce proper dye compartmentalization.</li>
                </ul>

                <h4 style="margin-bottom: 5px; color: var(--dark-slate);">Quality Control Representative Results</h4>
                <ul style="margin-left: 20px; margin-bottom: 15px; line-height: 1.6;">
                    <li><strong>Figure 1 (Microplate):</strong> Viable cells assessed via plate reader show distinct fluorescence intensity peaks at Ex: 490 nm / Em: 525 nm.</li>
                    <li><strong>Figure 2 (Microscopy):</strong> Epifluorescence images demonstrate live cells displaying green fluorescence due to successful intracellular conversion to calcein. (When counterstained with Hoechst, nuclei can be pseudocolored red for morphological clarity using appropriate filter sets).</li>
                </ul>
            """,
            download_link="/downloads/calcein-am-protocol.pdf"
        ),
        
        # --- CATEGORY 2: MICROSCOPY ---
        Product(
            name="Nova", 
            price=4200.00, 
            category_id=cat2.id,
            description="Anti-fade reagent for prolonged fluorescence preservation.",
            images = "Assets/mountingnova/C1-microscopy.lif - Series001.jpg,Assets/mountingnova/Composite.jpg",
            image_captions="Amber tubes ensure protection for light-sensitive dyes,Assay results demonstrating cell viability over 48 hours,Epifluorescence microscopy overlaid with Hoechst nuclear stain",
            specs_html="""
                <h3 style="margin-bottom: 10px; color: var(--dark-slate);">Product Overview</h3>
                <p>Our liquid mounting media is formulated to prevent rapid photobleaching of fluorescent proteins and dyes during microscopy. It cures to form a semi-permanent seal, allowing slides to be stored at 4°C for months without signal degradation.</p>
            """,
            protocol_html="""
                <ol style="margin-left: 20px; margin-bottom: 15px;">
                    <li>Remove excess moisture from the slide (do not let the tissue completely dry).</li>
                    <li>Apply 1-2 drops (approx. 20-40 µl) of mounting media directly to the sample.</li>
                    <li>Carefully lower the coverslip at an angle to avoid trapping air bubbles.</li>
                    <li>Allow to set for 2 hours at room temperature before imaging.</li>
                </ol>
            """,
            support_html="""
                <p><strong>Bubbles under coverslip:</strong> Usually caused by applying too little media or dropping the coverslip too quickly. If bubbles occur, apply gentle pressure to the center of the coverslip with a pipette tip to push them out before the media cures.</p>
            """,
            download_link="/downloads/mounting-media-specs.pdf"
        ),
        Product(
            name="Supernova", 
            price=850.00, 
            category_id=cat2.id,
            description="Self-sealing, hard-setting anti-fade mounting media retaining fluorescence for >5 months.",
            images ="Assets/supernova/MAX_Gagan R.jpg",
            image_captions="Amber tubes ensure protection for light-sensitive dyes,Assay results demonstrating cell viability over 48 hours,Epifluorescence microscopy overlaid with Hoechst nuclear stain",
            specs_html="""
                <h3 style="margin-bottom: 10px; color: var(--dark-slate);">Product Overview</h3>
                <p style="margin-bottom: 15px;"><strong>Supernova</strong> is a premium self-sealing, hard-setting anti-fade mounting media. Unlike liquid media that require manual sealing with adhesives, Supernova cures into a hardened state, retaining vivid specimen fluorescence for over 5 months from the date of preparation.</p>
                
                <h4 style="margin-bottom: 10px; color: var(--dark-slate);">Engineered for Optical Excellence</h4>
                <p style="margin-bottom: 10px;">Supernova was developed to meet all stringent criteria for high-performance mounting media:</p>
                <ul style="margin-left: 20px; margin-bottom: 15px;">
                    <li><strong>Optics:</strong> Refractive index close to glass (~1.5), perfectly transparent, and color-free.</li>
                    <li><strong>Integrity:</strong> Dries to a non-tacky state without crystallizing, cracking, shrinking, or pulling away from coverslip edges.</li>
                    <li><strong>Protection:</strong> Resists microbial growth, oxidation, and pH shifts without damaging or altering delicate tissue components or stains.</li>
                </ul>
            """,
            protocol_html="""
                <h4 style="margin-bottom: 8px; color: var(--dark-slate);">1. Mounting Procedure</h4>
                <ol style="margin-left: 20px; margin-bottom: 20px;">
                    <li>Carefully drain excess liquid from the coverslip containing the fixed or stained cells. <em>(Do not let the specimen dry completely).</em></li>
                    <li>Place an appropriate drop of mounting medium onto a clean glass slide. Adjust volume according to coverslip size to avoid overflow.</li>
                    <li>Gently invert the coverslip (cell side facing down) onto the drop of the mounting medium, taking care to avoid air bubble formation.</li>
                </ol>

                <h4 style="margin-bottom: 8px; color: var(--dark-slate);">2. Curing Conditions</h4>
                <ul style="margin-left: 20px; margin-bottom: 15px;">
                    <li><strong>Standard Curing:</strong> ~1 hour at room temperature in the dark (when humidity is below 75%).</li>
                    <li><strong>Accelerated Curing:</strong> Place slides in a dehumidified chamber.</li>
                    <li><strong>Imaging:</strong> Can begin after 1 hour of setting time. For improved stability and maximum fluorescence preservation, leave slides at room temperature for ≥8 hours before imaging.</li>
                </ul>
            """,
            support_html="""
                <h3 style="margin-bottom: 10px; color: var(--dark-slate);">Notes & Troubleshooting</h3>
                <ul style="margin-left: 20px; margin-bottom: 15px; line-height: 1.6;">
                    <li><strong>Photobleaching Prevention:</strong> Always perform mounting and curing steps in low light or complete darkness.</li>
                    <li><strong>Environmental Factors:</strong> Humidity significantly affects curing time. Use a dry or dehumidified environment for consistent, rapid results. Do not disturb slides during curing.</li>
                    <li><strong>Volume Control:</strong> Excess mounting medium can lead to leakage or slow curing. Use the optimal volume for your specific coverslip dimensions.</li>
                    <li><strong>Fluorophore Compatibility:</strong> Ensure your specific experimental fluorophores are compatible with hard-setting mountants prior to large-scale applications.</li>
                </ul>
            """,
            download_link="/downloads/supernova-datasheet.pdf"
        ),
        
        # --- CATEGORY 3: MYCOPLASMA ---
        Product(
            name="MaRK (Mycoplasma Removal Kit)", 
            price=420.00, 
            category_id=cat3.id,
            description="Specialized reagent designed for effective elimination of mycoplasma contamination in cell cultures, whether mild or heavy.",
            images = "Assets/mark/oflyer.JPG,Assets/mark/CA1a infected.2.jpg,Assets/mark/otreated 2.jpg",
            image_captions="Amber tubes ensure protection for light-sensitive dyes,Assay results demonstrating cell viability over 48 hours,Epifluorescence microscopy overlaid with Hoechst nuclear stain",
            specs_html="""
                <h3 style="margin-bottom: 10px; color: var(--dark-slate);">Product Information & Background</h3>
                <p style="margin-bottom: 15px;">MaRK is a sterile-filtered, cell culture-tested solution supplied at 10 mg/ml in three amber-colored tubes. It is designed to eradicate mycoplasma—small, cell-wall-lacking microorganisms that compromise cell metabolism and genetic integrity—without affecting mammalian cells.</p>
                
                <h4 style="margin-bottom: 10px; color: var(--dark-slate);">Mechanism of Action</h4>
                <ul style="margin-left: 20px; margin-bottom: 20px;">
                    <li><strong>Protein Synthesis Inhibitor:</strong> Disrupts protein production inside mycoplasma.</li>
                    <li><strong>DNA Gyrase Inhibitor:</strong> Systematically blocks mycoplasma-specific DNA replication[cite: 1].</li>
                </ul>
                
                <h4 style="margin-bottom: 5px; color: var(--dark-slate);">Storage & Quality Control</h4>
                <p><strong>Storage:</strong> Store at 4°C for up to 1 month, or at -20°C for long-term storage (18 months from manufacturing). Avoid repeated freeze-thaw cycles[cite: 1].</p>
                <p><strong>Tested Lines:</strong> Validated in MCF10A, MCF10AT, MCF10CA1a, MCF7, HEK293T, HEK293, X-lenti, C127I, Neuro2a, and HeLa[cite: 1].</p>
            """,
            protocol_html="""
                <h3 style="margin-bottom: 10px; color: var(--dark-slate);">Treatment Regimen</h3>
                <p style="margin-bottom: 15px;">The working concentration is 0.5–1.0 μl/ml. Ensure cells are in the exponential growth phase before treatment[cite: 1].</p>
                
                <h4 style="margin-bottom: 5px; color: var(--dark-slate);">1. Prepare Cells</h4>
                <ul style="margin-left: 20px; margin-bottom: 15px;">
                    <li>Remove contaminated medium and rinse cells twice with PBS to remove residual contaminants[cite: 1].</li>
                </ul>
                
                <h4 style="margin-bottom: 5px; color: var(--dark-slate);">2. Treatment Setup</h4>
                <ul style="margin-left: 20px; margin-bottom: 15px;">
                    <li>Split culture into fresh medium containing MaRK (Standard: 1.0 μl/ml)[cite: 1].</li>
                    <li>For sensitive lines, test concentrations between 0.6–1.2 μl/ml[cite: 1].</li>
                </ul>
                
                <h4 style="margin-bottom: 5px; color: var(--dark-slate);">3. Maintenance</h4>
                <p>Every 3-4 days, passage cells and replace with fresh MaRK-infused medium. Continue for 2 weeks to ensure complete elimination[cite: 1].</p>
            """,
            support_html="""
                <h3 style="margin-bottom: 10px; color: var(--dark-slate);">Troubleshooting & Verification</h3>
                <p style="margin-bottom: 15px;"><strong>Handling Infection Severity:</strong> Use 1.0 μl/ml for heavy loads (Figure 2) and 0.6 μl/ml for low loads. Always test cell tolerability with smaller volumes before scaling[cite: 1].</p>
                
                <p style="margin-bottom: 15px;"><strong>Verification:</strong> Confirm clearance using DAPI staining, mycoplasma detection kits, or colorimetric assays[cite: 1].</p>
                
                <div style="background: #fff8e1; border-left: 4px solid #ffb300; padding: 15px; border-radius: 4px;">
                    <strong>Technical Support:</strong> If contamination persists after 7 days, perform a facility clean-up and trace the source. For analytical questions, contact <a href="mailto:admin@olirumscience.com" style="color: var(--accent-blue); font-weight: 600;">admin@olirumscience.com</a>[cite: 1].
                </div>
            """,
            download_link="protocols/MaRK_Datasheet.pdf"
        ),
        Product(
            name="MAD™ qPCR Mycoplasma Detection Kit", 
            price=18500.00,
            category_id=cat3.id,
            description="Rapid, sensitive qPCR-based detection of up to 178 Mycoplasma species.",
            images = "Assets/mad/MaD flyer.jpg,Assets/mad/ML 2025-08-15 15h32m09s(Ethidium Bromide).jpg",
            image_captions="Amber tubes ensure protection for light-sensitive dyes,Assay results demonstrating cell viability over 48 hours,Epifluorescence microscopy overlaid with Hoechst nuclear stain",
            specs_html="""
                <h3 style="margin-bottom: 10px; color: var(--dark-slate);">Product Overview</h3>
                <p style="margin-bottom: 15px;">The Olirum MAD™ qPCR-based Mycoplasma Detection Kit enables rapid, sensitive detection of up to 178 Mycoplasma species in cell-culture samples, media, PBS, or other liquid specimens. All qPCR reagents—polymerase, primers, probes, dNTPs, and buffer—are pre-mixed; no additional reagents are needed. The workflow requires only sample pelleting, lysis, and direct qPCR setup.</p>
                
                <h4 style="margin-bottom: 5px; color: var(--dark-slate);">Materials Provided</h4>
                <ul style="margin-left: 20px; margin-bottom: 15px;">
                    <li><strong>qPCR Mix:</strong> Ready-to-use; contains polymerase, primers/probes, dNTPs, SYBR green, and buffer</li>
                    <li><strong>Lysis Solution:</strong> For sample lysis prior to qPCR</li>
                    <li><strong>Positive Control:</strong> Verified positive mycoplasma lysate for assay validation</li>
                </ul>
                
                <h4 style="margin-bottom: 5px; color: var(--dark-slate);">Storage and Stability</h4>
                <ul style="margin-left: 20px; margin-bottom: 15px;">
                    <li><strong>qPCR Mix:</strong> Store at −20 °C; avoid repeated freeze–thaw cycles.</li>
                    <li><strong>Lysis Solution:</strong> Store at room temperature or 4 °C.</li>
                    <li><strong>Positive Mycoplasma Lysate:</strong> Store at −20 °C or −80 °C; handle as potentially infectious.</li>
                    <li><strong>Prepared Sample Lysates:</strong> Store at −20 °C (short term) or −80 °C (long term).</li>
                </ul>
            """,
            protocol_html="""
                <h4 style="margin-bottom: 5px; color: var(--dark-slate);">1. Sample Preparation</h4>
                <ol style="margin-left: 20px; margin-bottom: 15px;">
                    <li><strong>Pellet the Sample:</strong> Transfer 200 µL of test sample into a 1.5 mL tube. Centrifuge at 11,000 RPM for 5 minutes. Carefully discard the supernatant. <em>(Proceed even if no visible pellet forms, as mycoplasma pellets are often transparent).</em></li>
                    <li><strong>Lysis:</strong> Add 50 µL Lysis Solution directly to the pellet/tube bottom. Mix thoroughly by pipetting or brief vortexing and incubate for 3 minutes. Heat at 95 °C for 5 minutes (or up to 10 mins) to lyse cells.</li>
                </ol>

                <h4 style="margin-bottom: 5px; color: var(--dark-slate);">2. qPCR Reaction Setup (20 µL total)</h4>
                <p style="margin-bottom: 10px;"><em>Prepare all reactions on ice. For multiple samples, prepare a master mix and aliquot 19 µL per reaction.</em></p>
                <ul style="margin-left: 20px; margin-bottom: 15px;">
                    <li><strong>qPCR Mix:</strong> 19 µL</li>
                    <li><strong>Lysate:</strong> 1 µL (Sample or control)</li>
                </ul>

                <h4 style="margin-bottom: 5px; color: var(--dark-slate);">3. qPCR Cycling Conditions</h4>
                <ul style="margin-left: 20px; margin-bottom: 15px;">
                    <li><strong>Initial Denaturation:</strong> 95 °C for 2 min (1 cycle)</li>
                    <li><strong>Denaturation:</strong> 95 °C for 5–10 s (40 cycles)</li>
                    <li><strong>Anneal / Extension:</strong> 60 °C for 30–60 s (40 cycles) - <em>Collect fluorescence at the end of each 60 °C step.</em></li>
                </ul>
            """,
            support_html="""
                <h4 style="margin-bottom: 5px; color: var(--dark-slate);">Result Interpretation</h4>
                <ul style="margin-left: 20px; margin-bottom: 15px;">
                    <li><strong>Positive Sample:</strong> Amplification curve with Ct &lt; 35</li>
                    <li><strong>Negative Sample:</strong> No amplification (Ct &gt; 40 or undetermined)</li>
                    <li><strong>Positive Control:</strong> Clear amplification at expected Ct (typically 20–30)</li>
                    <li><strong>NTC / Blank:</strong> No amplification</li>
                </ul>

                <h4 style="margin-bottom: 5px; color: var(--dark-slate);">Recommended Controls</h4>
                <ul style="margin-left: 20px; margin-bottom: 20px;">
                    <li><strong>Positive Control (1 µL lysate):</strong> Confirms assay and reagent performance.</li>
                    <li><strong>Negative Control (1 µL Nuclease-free water):</strong> Detects contamination.</li>
                    <li><strong>Extraction Blank (1 µL lysis solution):</strong> Monitors contamination introduced during prep.</li>
                </ul>
                
                <div style="background: #fff8e1; border-left: 4px solid #ffb300; padding: 15px; border-radius: 4px;">
                    <strong>Troubleshooting & Support:</strong> If controls do not perform as expected, repeat the run after checking reagent integrity and pipetting accuracy. For technical support, contact <a href="mailto:olirumscientific@gmail.com" style="color: var(--accent-blue); font-weight: 600;">olirumscientific@gmail.com</a>.
                </div>
            """,
            download_link="/downloads/mad-protocol.pdf"
        ),
        
    ]

    # 4. Save everything down permanently
    db.add_all(products)
    db.commit()
    print("✅ Success! Database wiped and completely rebuilt with rich text technical specs.")

except Exception as e:
    print(f"❌ Error during database seeding: {e}")
finally:
    db.close()

# commented out
    # Product(
    #         name="FAVA (Fluorescent Assay for Viability)", 
    #         price=8500.00, 
    #         category_id=cat1.id,
    #         description="High-throughput cellular viability assay utilizing cell-permeable fluorogenic dyes.",
    #         specs_html="""
    #             <h3 style="margin-bottom: 10px; color: var(--dark-slate);">Product Overview</h3>
    #             <p style="margin-bottom: 15px;">This assay utilizes a cell-permeable fluorogenic dye that is converted by intracellular esterases into highly fluorescent calcein within live cells, providing a robust, direct indicator of cell viability.</p>
    #             <ul style="margin-left: 20px; margin-bottom: 20px;">
    #                 <li><strong>Excitation / Emission:</strong> 490 nm / 525 nm</li>
    #                 <li><strong>Recommended Working Concentration:</strong> 0.5 µM</li>
    #                 <li><strong>Applications:</strong> Microplate reader assays and Epifluorescence microscopy</li>
    #             </ul>
    #         """,
    #         protocol_html="""
    #             <h4 style="margin-bottom: 5px; color: var(--dark-slate);">1. Reagent Preparation</h4>
    #             <ul style="margin-left: 20px; margin-bottom: 15px;">
    #                 <li><strong>Stock Solution (1 mM):</strong> Reconstitute the 50 µg vial with 50 µL Dimethyl sulfoxide (DMSO). Mix gently until completely dissolved. Aliquot if necessary and store at −20°C protected from light. Avoid repeated freeze–thaw cycles.</li>
    #                 <li><strong>Working Solution (0.5 µM):</strong> Dilute 1 µL of 1 mM stock into 1999 µL assay buffer, PBS, or serum-free culture medium immediately before use. Protect from light.</li>
    #             </ul>

    #             <h4 style="margin-bottom: 5px; color: var(--dark-slate);">2. 96-Well Plate Fluorescence Assay</h4>
    #             <ol style="margin-left: 20px; margin-bottom: 15px;">
    #                 <li><strong>Cell Seeding:</strong> Seed cells at densities of 1 × 10³ – 5 × 10⁵ cells/mL (100 µL per well). Incubate overnight for adherent cell lines to attach.</li>
    #                 <li><strong>Dye Loading:</strong> Remove culture medium if required. Add 100 µL fresh assay buffer, then add the working solution to achieve a final well concentration of 0.5 µM.</li>
    #                 <li><strong>Incubation:</strong> Incubate the plate at 37°C for 30 minutes in the dark. <em>(Typical optimal range: 20 minutes to 1 hour).</em></li>
    #                 <li><strong>Washing:</strong> Remove dye-containing buffer. Wash cells 1–2 times with indicator-free assay buffer to remove excess probe.</li>
    #                 <li><strong>Measurement:</strong> Record fluorescence intensity using a microplate reader (Excitation: 490 nm | Emission: 525 nm | Cutoff: 515 nm).</li>
    #             </ol>
    #         """,
    #         support_html="""
    #             <h4 style="margin-bottom: 5px; color: var(--dark-slate);">Notes & Optimization</h4>
    #             <ul style="margin-left: 20px; margin-bottom: 15px;">
    #                 <li><strong>Background Interference:</strong> Phenol red and serum esterases in standard culture media may contribute to background fluorescence. Using clear, serum-free buffers is highly recommended during measurement.</li>
    #                 <li><strong>Protocol Adjustments:</strong> Optimal incubation time varies heavily depending on cell type and density. Note that lower incubation temperatures may reduce proper dye compartmentalization.</li>
    #             </ul>

    #             <h4 style="margin-bottom: 5px; color: var(--dark-slate);">Quality Control Representative Results</h4>
    #             <ul style="margin-left: 20px; margin-bottom: 15px; line-height: 1.6;">
    #                 <li><strong>Figure 1 (Microplate):</strong> Viable cells assessed via plate reader show distinct fluorescence intensity peaks at Ex: 490 nm / Em: 525 nm.</li>
    #                 <li><strong>Figure 2 (Microscopy):</strong> Epifluorescence images demonstrate live cells displaying green fluorescence due to successful intracellular conversion to calcein. (When counterstained with Hoechst, nuclei can be pseudocolored red for morphological clarity using appropriate filter sets).</li>
    #             </ul>
    #         """,
    #         download_link="/downloads/fava-protocol.pdf"
    #     ),