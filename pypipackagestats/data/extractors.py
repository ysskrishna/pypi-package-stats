from nestedutils import get_path


def get_upload_time(pkg_data: dict) -> str:
    """Extract upload_time from package data"""
    version = get_path(pkg_data, "info.version")
    
    if version:
        # Try to get upload_time from the first release file
        # Use list path to safely handle version strings that might contain special characters
        upload_time = get_path(pkg_data, ["releases", version, 0, "upload_time"])
        if not upload_time:
            upload_time = get_path(pkg_data, ["releases", version, 0, "upload_time_iso_8601"])
        if upload_time:
            return upload_time
    
    return ""

