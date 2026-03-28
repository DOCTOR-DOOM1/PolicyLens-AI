from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

print("🚀 Injecting the Ultimate Golden Dataset into ChromaDB...")

golden_schemes = [
    # --- STUDENT & SCHOLARSHIP SCHEMES ---
    Document(page_content="**PM Post-Matric Scholarship**\nEligibility: Students from SC/ST/OBC categories studying in class 11, 12, or college (including Engineering/Medical). Annual family income must be below ₹2,50,000.\nBenefits: Covers tuition fees, maintenance allowance, and study materials.", metadata={"source": "golden_dataset", "state": "Central"}),
    Document(page_content="**AICTE Pragati Scholarship for Girls**\nEligibility: Girl students admitted to first-year degree/diploma in an AICTE approved engineering college. Maximum two girls per family. Family income below ₹8,00,000.\nBenefits: ₹50,000 per annum for every year of study.", metadata={"source": "golden_dataset", "state": "Central"}),
    Document(page_content="**National Means-cum-Merit Scholarship (NMMS)**\nEligibility: Students in class 9 to 12. Family income must be strictly below ₹3,50,000. Must have scored 55% in 8th grade.\nBenefits: ₹12,000 per annum to arrest dropouts at the secondary stage.", metadata={"source": "golden_dataset", "state": "Central"}),
    Document(page_content="**Begum Hazrat Mahal National Scholarship**\nEligibility: Meritorious girl students belonging to minority communities (Muslim, Christian, Sikh, Buddhist, Parsi, Jain) studying in Classes 9 to 12. Family income below ₹2,00,000.\nBenefits: Admission and tuition fee coverage up to ₹10,000.", metadata={"source": "golden_dataset", "state": "Central"}),
    Document(page_content="**Mukhyamantri Yuva Swavalamban Yojana (MYSY)**\nEligibility: Students pursuing higher education (Engineering, Medical) who scored 80+ percentile in Class 12. Family income below ₹6,00,000.\nBenefits: 50% of tuition fees covered up to ₹50,000 per year.", metadata={"source": "golden_dataset", "state": "Gujarat"}),
    Document(page_content="**PM Vidyalaxmi Scheme**\nEligibility: Students securing admission in top 860 Qs/NIRF ranked institutions. Family income up to ₹8,00,000 for interest subvention.\nBenefits: Collateral-free, guarantor-free education loans up to ₹7.5 lakhs with 75% credit guarantee.", metadata={"source": "golden_dataset", "state": "Central"}),

    # --- FARMER & AGRICULTURE SCHEMES ---
    Document(page_content="**Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)**\nEligibility: All landholding farmer families with cultivable land in their name. No age limit.\nBenefits: Direct income support of ₹6,000 per year transferred in three equal installments.", metadata={"source": "golden_dataset", "state": "Central"}),
    Document(page_content="**PM Fasal Bima Yojana (Crop Insurance)**\nEligibility: All farmers growing notified crops in a notified area, including sharecroppers and tenant farmers.\nBenefits: Comprehensive insurance cover against failure of the crop, with premium as low as 1.5% to 2%.", metadata={"source": "golden_dataset", "state": "Central"}),
    Document(page_content="**Namo Shetkari Maha Samman Nidhi**\nEligibility: Farmers in Maharashtra who are already beneficiaries of the central PM-KISAN scheme.\nBenefits: An additional ₹6,000 per year, bringing the total annual support to ₹12,000.", metadata={"source": "golden_dataset", "state": "Maharashtra"}),

    # --- WOMEN & CHILD SCHEMES ---
    Document(page_content="**Mukhyamantri Majhi Ladki Bahin Yojana**\nEligibility: Women residing in Maharashtra, aged 21 to 65 years. Family income must be less than ₹2.5 lakh per annum.\nBenefits: Monthly financial assistance of ₹1,500 transferred directly to their bank accounts.", metadata={"source": "golden_dataset", "state": "Maharashtra"}),
    Document(page_content="**Sukanya Samriddhi Yojana**\nEligibility: Parents/guardians of a girl child below 10 years of age.\nBenefits: High-interest savings account (currently around 8.2%) with tax benefits under Section 80C to build a fund for the child's education and marriage.", metadata={"source": "golden_dataset", "state": "Central"}),
    Document(page_content="**PM Ujjwala Yojana**\nEligibility: Adult women belonging to BPL (Below Poverty Line) households, SC/ST, or forest dwellers.\nBenefits: Free LPG gas connection and the first refill completely free.", metadata={"source": "golden_dataset", "state": "Central"}),
    Document(page_content="**PM Matru Vandana Yojana**\nEligibility: Pregnant women and lactating mothers for their first living child. Should not be in regular government employment.\nBenefits: ₹5,000 cash incentive paid in three installments for maternal health and nutrition.", metadata={"source": "golden_dataset", "state": "Central"}),

    # --- BUSINESS, YOUTH & EMPLOYMENT SCHEMES ---
    Document(page_content="**PM MUDRA Yojana**\nEligibility: Any Indian citizen with a business plan for a non-farm sector income-generating activity (manufacturing, processing, trading, or service sector).\nBenefits: Collateral-free micro-credit loans up to ₹10 Lakhs (Shishu, Kishore, and Tarun categories).", metadata={"source": "golden_dataset", "state": "Central"}),
    Document(page_content="**Stand-Up India Scheme**\nEligibility: SC/ST and/or women entrepreneurs above 18 years. Must be setting up a greenfield (new) enterprise.\nBenefits: Bank loans between ₹10 lakh and ₹1 Crore to set up a manufacturing, trading, or service business.", metadata={"source": "golden_dataset", "state": "Central"}),
    Document(page_content="**PM Vishwakarma Yojana**\nEligibility: Traditional artisans and craftspeople (carpenters, blacksmiths, goldsmiths, potters, tailors, etc.) above 18 years.\nBenefits: Recognition certificate, ID card, skill training with ₹500/day stipend, free toolkit up to ₹15,000, and collateral-free credit up to ₹3 lakhs.", metadata={"source": "golden_dataset", "state": "Central"}),
    Document(page_content="**Chief Minister's Fellowship Program**\nEligibility: Graduates aged 21 to 26 years with at least 60% marks and 1 year of work experience. Must possess basic computer knowledge.\nBenefits: ₹75,000 monthly stipend to work directly with the state administration for 11 months.", metadata={"source": "golden_dataset", "state": "Maharashtra"}),

    # --- HEALTH, HOUSING & SOCIAL SECURITY ---
    Document(page_content="**Ayushman Bharat (PM-JAY)**\nEligibility: Poor, deprived rural families and identified occupational categories of urban workers (unemployed, low income). No age or family size limit.\nBenefits: Health insurance cover of ₹5,00,000 per family per year for secondary and tertiary care hospitalization.", metadata={"source": "golden_dataset", "state": "Central"}),
    Document(page_content="**PM Awas Yojana (Urban & Rural)**\nEligibility: Homeless families or those living in kutcha houses. Beneficiary family should not own a pucca house anywhere in India. Income limits apply for urban subsidies.\nBenefits: Financial assistance to build a pucca house or interest subsidy on home loans.", metadata={"source": "golden_dataset", "state": "Central"}),
    Document(page_content="**Atal Pension Yojana**\nEligibility: Any Indian citizen aged 18 to 40 years with a savings bank account. Primarily for the unorganized sector.\nBenefits: Guaranteed minimum monthly pension of ₹1,000 to ₹5,000 after reaching the age of 60, depending on contributions.", metadata={"source": "golden_dataset", "state": "Central"}),
    Document(page_content="**Gruha Jyothi Scheme**\nEligibility: All residential households in Karnataka.\nBenefits: Free electricity up to 200 units per month.", metadata={"source": "golden_dataset", "state": "Karnataka"}),
    Document(page_content="**Anna Bhagya Yojana**\nEligibility: BPL and Antyodaya cardholders in Karnataka.\nBenefits: 10 kg of free food grains (rice) per person per month to ensure food security.", metadata={"source": "golden_dataset", "state": "Karnataka"})
]

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(golden_schemes, embeddings, persist_directory="./chroma_db")

print(f"✅ BOOM! Successfully injected {len(golden_schemes)} elite schemes into your AI Brain!")