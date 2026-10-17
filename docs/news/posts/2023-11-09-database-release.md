---
title: Database release
date: 2023-11-09
categories:
- Database
- Release
slug: 2023-11-09-database-release
---

This month's data release features recent FDA approvals, updates of mutational signatures from version 2 to 3.4, updates to the source fields for several citations, removal of several entries, revising format of all clinical guideline citations, and the `publication_date` field has been populated for all current database records.

<!-- more -->

[View on GitHub](https://github.com/vanallenlab/moalmanac-db/releases/tag/v.2023-11-09)

Database content: v.2023-11-09
Database schema: 1.2.0

Added entries:

- (FDA) _BCR_::_ABL1_ and sensitivity to bosutinib for pediatric patients with CML.
- (FDA) _BRAF_ p.V600E and sensitivity to encorafenib in combination with binimetinib for adult patients with NSCLC.
- (FDA) _IDH1_ p.R132C, p.R132H, and somatic variants and sensitivity to ivosidenib for patients with myelodysplastic syndromes (MDS).
- (Guideline) _FLT3_ p.D835A, p.D835E, p.D835H, p.D835Y and poor prognosis in patients with MDS.
- (Guideline) _GATA2_ missense, nonsense, frameshift, and splice site variants and poor prognosis in patients with MDS.
- (Guideline) _NPM1_ p.W288Cfs*12 and poor prognosis in patients with MDS.
- (Guideline) _NRAS_ p.G12A, p.G12C, p.G12D, p.G12R, p.G12S, p.G12V, p.G13A, p.G13D, p.G13R, p.G13V, p.Q61E, p.Q61H, p.Q61L, p.Q61P, and p.Q61R and poor prognosis for patients with MDS.
- (Guideline) _SETBP1_ p.I865N and poor prognosis for patients with MDS.
- (Guideline) _SF3B1_ p.I704S and poor prognosis for patients with MDS.
- (Guideline) _SRSF2_ p.P95A, p.P95H, p.P95L, p.P95R, and p.P95_R102del and poor prognosis for patients with MDS.
- (Guideline) _TP53_ missense, nonsense, splice site, and frameshift variants and poor prognosis for patients with MDS.
- (Guideline) _U2AF1_ p.S34A, p.S34F, p.S34Y, p.Q157P, p.Q157R and poor prognosis for patients with MDS.

Revised entries:

- (FDA) _NTRK1/2/3_ fusions and sensitivity to entrectinib were revised due to the FDA's approval for adult or pediatric patients older than 1 month with any solid tumor.
- (Guideline) _PDGFRB_ translocations and sensitivity to imatinib in mds was revised to match updated guidelines that specify ETV6 as a fusion partner and CMML as a more specific tumor type.
- (Guideline) _TET2_ variants and sensitivity to Azacitidine was downgraded from Guideline to Clinical evidence.
- (Preclinical) _BRAF_ p.V600E and sensitivity to dabrafenib in combination with either omipalisib (PI3K/Akt/mTOR) or bevacizumab (VEGF/VEGFR) was revised to add clinical context and expand upon the relationship description.  
- All Mutational Signature relationships (17) have been updated from version 2 to version 3.4.
- The citation text was updated for Bostner et al. 2007 (PMID: 7486065), Leone et al. 2008 (PMID: 18829482), Corcoran et al. 2010 (PMID: 21098728), Sillars-Hardebol et al. 2012 (PMID: 22207630), Dickson et al. 2013 (PMID: 23569312), Etemadmoghadam et al. 2013 (PMID: 24218601), Johung et al. 2013 (PMID: 23897899), Van Allen et al. 2014 (PMID: 25096233), Wagle et al. 2014 (PMID: 24265154), Gorre et al. 2016 (PMID: 11423618), Luo et al. 2016 (PMID: 27580028), Cuppens et al. 2017 (PMID: 28232476), and Willliams et al. 2020 (PMID: 28283584).
- The DOI and/or URL were updated for Takano et al. 2005 (PMID: 15998907), Fong et al. 2009 (PMID: 19553641), Tesser-Gamba et al. 2012 (PMID: 22154052), Chatterjee et al. 2013 (PMID: 23565244), Hunter et al. 2014 (PMID: 24937673), Mak et al. 2015 (PMID: 25450872), Fondello et al. 2016 (PMID: 27399807), Hugo et al. 2016 (PMID: 26997480), Ke et al. 2016 (PMID: 27717507), Sung et al. 2016 (PMID: 27793752), George et al. 2017 (PMID: 28228279), Mouw et al. 2017 (PMID: 28630051), Aldubayan et al. 2018 (PMID: 29478780), Seligson et al. 2018 (PMID: 30541756), De Bono et al. 2019, and Tewari et al. 2021 (PMID: 34496240). Many of these changes are due to a recently discovered issue with DOIs pointing to journals published through Elsevier.
- The NCT code was updated for Le et al. 2015 (PMID: 26028255)

Removed entries,

- (Guideline) _BCR::ABL1_ and sensitivity to dasatinib, imatinib, and nilotinib in CML to reduce redundency from other CML guideline entries.
- (Guideline) _BRAF_ p.V600E and sensitivity to dabrafenib in combination with trametinib in patients with NSCLC. This citation was incorrectly categorized as a Guideline as it references an FDA approval, which has since been added to the knowledge base.  
- (Guideline) _BRCA1/2_ germline variants and sensitivity to pazopanib in ovarian cancer because the underlying source does not mention this relationship in the context of BRCA1/2.
- (Guideline) _BRCA2_ germline variants and sensitivity to olaparib in ovarian cancer, as there was a duplicate record.
- (Guideline) _KIT_ variants and poor prognosis in head and neck mucosal melanoma, as the citation suggests that head and neck mucosal melanoma has a poor prognosis independent of _KIT_ status.
- (Guideline) _KRAS_, _PRFPF8_variants and poor prognosis in MDS. While KRAS is included in the IPSS-M Prognostic Risk Schema, KRAS being highlight as associated with poor prognosis is not explicitly stated in current guidelines.
- (Guideline) _NRAS_, _SETBP1_, _TP53_ variants and poor prognosis in MDS has been removed as the current guidelines cite specific amino acid changes, which have been added.
- (Clinical trial) _EGFR_ variants and sensitivity to Durvalumab + Gefitinib in NSCLC was removed [per further studies](https://pubmed.ncbi.nlm.nih.gov/33012782/) observing a negative finding.
- (Clinical trial) _KRAS_ p.G12C and sensitivity to AMG 510 was removed because there are now associated FDA approvals, and we will be phasing out abstracts from the knowledge base.
- (Clinical evidence) _NRAS_ p.Q61L and sensitivity to Selumetinib in MDS was removed as it contained a duplicate record.
- (Preclinical) _BRAF_ p.V600E and sensitivity to GANT61 was removed because the study findings were independent of melanoma cell line BRAF or NRAS status.
