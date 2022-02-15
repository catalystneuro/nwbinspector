"""Check functions that examine general NWBFile metadata."""
from pynwb import NWBFile

from ..register_checks import register_check, InspectorMessage, Importance


@register_check(importance=Importance.BEST_PRACTICE_SUGGESTION, neurodata_type=NWBFile)
def check_experimenter(nwbfile: NWBFile):
    """Check if an experimenter has been added for the session."""
    if not nwbfile.experimenter:
        return InspectorMessage(message="Experimenter is missing.")


@register_check(importance=Importance.BEST_PRACTICE_SUGGESTION, neurodata_type=NWBFile)
def check_experiment_description(nwbfile: NWBFile):
    """Check if a description has been added for the session."""
    if not nwbfile.experiment_description:
        return InspectorMessage(message="Experiment description is missing.")


@register_check(importance=Importance.BEST_PRACTICE_SUGGESTION, neurodata_type=NWBFile)
def check_institution(nwbfile: NWBFile):
    """Check if a description has been added for the session."""
    if not nwbfile.institution:
        return InspectorMessage(message="Metadata /general/institution is missing.")


# @nwbinspector_check(severity=1, neurodata_type=NWBFile)
# def check_keywords(nwbfile: NWBFile):
#     """Check if keywords have been added for the session."""
#     if not nwbfile.keywords:
#         return "Metadata /general/keywords is missing!"


# @nwbinspector_check(severity=1, neurodata_type=NWBFile)
# def check_doi_publications(nwbfile: NWBFile):
#     """Check if related_publications have been added as doi links."""
#     valid_starts = ["doi:", "http://dx.doi.org/", "https://doi.org/"]
#     if nwbfile.related_publications:
#         for publication in nwbfile.related_publications:
#             if any([publication.startswith(valid_start) for valid_start in valid_starts]):
#                 return f"Metadata /general/related_publications '{publication}' does not include 'doi'!"


# @nwbinspector_check(severity=1, neurodata_type=NWBFile)
# def check_subject_sex(nwbfile: NWBFile):
#     """Check if the subject sex has been specified, if one exists."""
#     if nwbfile.subject and not nwbfile.subject.sex:
#         return "Metadata /general/subject/sex is missing!"


# @nwbinspector_check(severity=2, neurodata_type=NWBFile)
# def check_subject_id(nwbfile: NWBFile):
#     """
#     Check if the subject ID has been specified, if one exists.

#     This is a metadata requirement for upload to the DANDI archive.
#     """
#     if nwbfile.subject and not nwbfile.subject.subject_id:
#         return "Metadata /general/subject/subject_id is missing!"


# @nwbinspector_check(severity=2, neurodata_type=NWBFile)
# def check_subject_species(nwbfile: NWBFile):
#     """Check if the subject species has been specified, if one exists."""
#     if nwbfile.subject and not nwbfile.subject.species:
#         return "Metadata /general/subject/species is missing!"
