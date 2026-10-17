# Algorithm

The MOAlmanac algorithm ([moalmanac](https://github.com/vanallenlab/moalmanac)) is a clinical interpretation algorithm that annotates and evaluates whole-exome and transcriptome data from individual patient samples, using the [database](../database/index.md) as its knowledge base. It can:

- Identify mutations and genomic features related to therapeutic sensitivity and resistance, and of prognostic relevance.
- Annotate somatic and germline variants against several datasources.
- Sort and evaluate somatic single nucleotide variants, insertions and deletions, copy number alterations and fusions by clinical and biological relevance.
- Integrate data types to see which genes are altered in both the somatic and germline setting.
- Extract and evaluate germline variants relevant to adult and hereditary cancers.
- Identify overlap between somatic variants observed in DNA and RNA, or in any other validation sequencing.
- Identify variants that may be related to microsatellite stability.
- Calculate coding mutational burden and compare a patient to TCGA.
- Identify genomic features that may be related to one another.
- Create portable web-based actionability reports summarizing clinically relevant findings.

## Running it

The algorithm is available from its [GitHub repository](https://github.com/vanallenlab/moalmanac), as a [Docker image](https://hub.docker.com/r/vanallenlab/moalmanac/), and as a [Terra workflow](https://app.terra.bio/#workflows/vanallenlab/moalmanac). Running it from GitHub requires building some of its datasources, which the Docker image already contains. See the repository's README for installation and usage.

## Inputs and outputs

- [Description of inputs](description-of-inputs.md): every required and optional argument, with the expected file formats and columns.
- [Description of outputs](description-of-outputs.md): every file the algorithm produces, and the columns they share.

Both pages are copied from the algorithm repository's `docs/` folder.
