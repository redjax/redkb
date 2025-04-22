---
tags:
    - python
    - controllers
    - snippets
    - s3
    - minio
---

# Minio

Class controller for interacting with [minio S3 storage](https://min.io/docs/minio/linux/developers/python/minio-py.html).

This script is a CLI, run it with `--help` to see usage instructions. The controller can load Minio configuration from CLI args, or from a JSON configuration file. The script accepts `-g`/`--generate-configs` as an arg, which will create dummy versions of a `minio_config.json` and various "job" files that you can edit for your needs.

The script can be dropped into an existing app so you can import pieces of it into other scripts/packages, or it can be used as a standalone CLI. The `# /// script` portion at the top of the file informs [`uv`](https://docs.astral.sh/uv/guides/scripts/#declaring-script-dependencies) and other package managers on which dependencies the script requires. This is called [inline script metadata](https://packaging.python.org/en/latest/specifications/inline-script-metadata/#script-type), and is a built-in feature of the Python language. This was introduced to the language in [PEP 723](https://peps.python.org/pep-0723/).

`uv` will automatically detect the inline metadata when you run this script with `uv run script_name.py`, and will install the packages declared at the top of the file.

```python title="MinioController.py" linenums="1"
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "minio",
# ]
# ///

from __future__ import annotations

from dataclasses import dataclass, field
import glob
import logging
import os
from pathlib import Path
import typing as t

from minio import Minio
from minio.commonconfig import CopySource
from minio.deleteobjects import DeleteObject
from minio.error import S3Error

log = logging.getLogger(__name__)

__all__ = [
    "MinioController",
    "get_minio_controller",
    "MinioSettings",
    "MinioJob",
    "MinioUploadJob",
    "MinioDownloadJob",
    "MinioDeleteJob",
    "MinioCopyJob",
    "MinioMoveJob",
]


@dataclass
class MinioSettings:
    endpoint: str
    access_key: str
    secret_key: str = field(default=None, repr=False)
    secure: bool = field(default=True)
    cert_check: bool = field(default=True)


@dataclass
class MinioJob:
    """Base class for all Minio jobs."""

    type: str
    bucket: str


@dataclass
class MinioCopyMoveJobBase(MinioJob):
    remote_path: str
    remote_dest: str
    dest_bucket: str


@dataclass
class MinioUploadJob(MinioJob):
    remote_path: str
    local_path: str


@dataclass
class MinioDownloadJob(MinioJob):
    remote_path: str
    local_path: str


@dataclass
class MinioDeleteJob(MinioJob):
    remote_path: str


@dataclass
class MinioCopyJob(MinioCopyMoveJobBase):
    pass


@dataclass
class MinioMoveJob(MinioCopyMoveJobBase):
    pass


class MinioConfigGenerator:
    """Generates a default MinIO configuration JSON file."""

    def __init__(self, output_path: str = "minio_conf.json"):
        self.output_path = output_path
        self.default_config = {
            "endpoint": "<ip:9000 or FQDN>",
            "access_key": "<minio access key>",
            "secret_key": "<minio secret key>",
            "secure": True,
            "cert_check": False,
        }

        self.logger = log.getChild("MinioConfigGenerator")

    def generate(self):
        """Generates the MinIO config JSON file if it doesn't exist."""
        if not Path(self.output_path).exists() or not Path(self.output_path).is_file():
            with open(self.output_path, "w") as f:
                json.dump(self.default_config, f, indent=4)
            self.logger.info(f"Generated default MinIO config at {self.output_path}")
        else:
            self.logger.warning(f"MinIO config already exists at {self.output_path}")


class MinioJobConfigGenerator:
    """Base class for generating default MinIO job configuration JSON files."""

    def __init__(self, job_type: str, output_path: str = "job.TYPE.json"):
        self.job_type = job_type
        self.output_path = output_path.replace("TYPE", self.job_type)

        self.logger = log.getChild("MinioJobConfigGenerator")

    def generate(self):
        """Generates the job config JSON file if it doesn't exist."""
        if not Path(self.output_path).exists() or not Path(self.output_path).is_file():
            with open(self.output_path, "w") as f:
                json.dump(self.default_config, f, indent=4)
            self.logger.info(
                f"Generated default {self.job_type} job config at {self.output_path}"
            )
        else:
            self.logger.warning(
                f"{self.job_type} job config already exists at {self.output_path}"
            )


class MinioUploadJobGenerator(MinioJobConfigGenerator):
    """Generates a default MinIO upload job configuration JSON file."""

    def __init__(self, output_path: str = "job.TYPE.json"):
        super().__init__("upload", output_path)

        self.default_config = {
            "type": "upload",
            "bucket": "<minio bucket>",
            "remote_path": "<minio path>",
            "local_path": "<local path>",
        }


class MinioDownloadJobGenerator(MinioJobConfigGenerator):
    """Generates a default MinIO download job configuration JSON file."""

    def __init__(self, output_path: str = "job.TYPE.json"):
        super().__init__("download", output_path)

        self.default_config = {
            "type": "download",
            "bucket": "<minio bucket>",
            "remote_path": "<minio path>",
            "local_path": "<local path>",
        }


class MinioDeleteJobGenerator(MinioJobConfigGenerator):
    """Generates a default MinIO delete job configuration JSON file."""

    def __init__(self, output_path: str = "job.TYPE.json"):
        super().__init__("delete", output_path)

        self.default_config = {
            "type": "delete",
            "bucket": "<minio bucket>",
            "remote_path": "<minio path>",
        }


class MinioCopyJobGenerator(MinioJobConfigGenerator):
    """Generates a default MinIO copy job configuration JSON file."""

    def __init__(self, output_path: str = "job.TYPE.json"):
        super().__init__("copy", output_path)

        self.default_config = {
            "type": "copy",
            "bucket": "<minio bucket>",
            "remote_path": "<minio path>",
            "remote_dest": "<minio dest path>",
            "dest_bucket": "<minio dest bucket>",
        }


class MinioMoveJobGenerator(MinioJobConfigGenerator):
    """Generates a default MinIO move job configuration JSON file."""

    def __init__(self, output_path: str = "job.TYPE.json"):
        super().__init__("move", output_path)

        self.default_config = {
            "type": "move",
            "bucket": "<minio bucket>",
            "remote_path": "<minio path>",
            "remote_dest": "<minio dest path>",
            "dest_bucket": "<minio dest bucket>",
        }


def parse_args() -> argparse.Namespace:
    """Call this function to parse input args from the command line."""
    parser = argparse.ArgumentParser(
        description="CLI for uploading files & directories to minio."
    )

    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument(
        "-g", "--generate-configs", action="store_true", help="Generate default configs"
    )
    parser.add_argument(
        "-c",
        "--minio-config",
        type=str,
        help="Path to minio config file. Default: minio_conf.json",
        default="minio_conf.json",
    )
    parser.add_argument(
        "-j",
        "--job-file",
        type=str,
        help="Path to a JSON file describing an upload/download job.",
    )
    parser.add_argument(
        "-e",
        "--minio-endpoint",
        type=str,
        help="Minio endpoint",
    )
    parser.add_argument("-ak", "--minio-access-key", type=str, help="Minio access key")
    parser.add_argument("-sk", "--minio-secret-key", type=str, help="Minio secret key")
    parser.add_argument("-b", "--bucket", type=str, help="Minio bucket to upload to")
    parser.add_argument(
        "-l", "--local-path", type=str, help="Local path to upload to minio"
    )
    parser.add_argument("-t", "--minio-path", type=str, help="Minio path to upload to")
    parser.add_argument("--secure", action="store_true", help="Use secure connection")
    parser.add_argument("--check-cert", action="store_true", help="Check certificate")

    args = parser.parse_args()

    return args


def generate_default_configs():
    log.info("Generating default configurations")

    try:
        MinioConfigGenerator().generate()
        MinioUploadJobGenerator().generate()
        MinioDownloadJobGenerator().generate()
        MinioDeleteJobGenerator().generate()
        MinioCopyJobGenerator().generate()
        MinioMoveJobGenerator().generate()
    except Exception as e:
        log.error(f"Error generating default configs: {e}")


def load_minio_job(
    job_file: str,
) -> t.Union[
    MinioCopyJob, MinioMoveJob, MinioDeleteJob, MinioUploadJob, MinioDownloadJob
]:
    """Loads a Minio job from a JSON file and returns the appropriate dataclass.

    Params:
        job_file (str): Path to the JSON job file.

    Returns:
        MinioJob: An instance of the appropriate MinioJob dataclass.

    """
    job_file = normalize_path(job_file)

    with open(job_file, "r") as f:
        job_data = json.load(f)

    job_type = job_data.get("type")
    if not job_type:
        raise ValueError("Job file must contain a 'type' field.")

    if job_type == "upload":
        return MinioUploadJob(**job_data)
    elif job_type == "download":
        return MinioDownloadJob(**job_data)
    elif job_type == "delete":
        return MinioDeleteJob(**job_data)
    elif job_type == "copy":
        return MinioCopyJob(**job_data)
    elif job_type == "move":
        return MinioMoveJob(**job_data)
    else:
        raise ValueError(f"Unsupported job type: {job_type}")


def get_minio_controller(
    endpoint: str,
    access_key: str,
    secret_key: str,
    secure: bool = True,
    cert_check: bool = True,
) -> "MinioController":
    """Initializes a MinioController instance.

    Params:
        endpoint (str): Minio endpoint.
        access_key (str): Minio access key.
        secret_key (str): Minio secret key.
        secure (bool): Whether to use SSL.
        cert_check (bool): Whether to verify SSL certificates.

    Returns:
        (MinioController): A controller class to handle minio operations.

    """
    try:
        ## Intialize MinioController instance
        controller: MinioController = MinioController(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
            cert_check=cert_check,
        )

        return controller
    except Exception as e:
        log.error(f"Error initializing MinioController: {e}")
        raise


def normalize_path(path: t.Union[str, Path]) -> str:
    """Converts a local or remote path to a normalized path (forward slashes '/').

    Params:
        path (str): Local or remote path.

    Returns:
        (str): Normalized path.

    """
    if not isinstance(path, Path) and not isinstance(path, str):
        raise TypeError(f"Expected str or Path, got {type(path)}")

    ## Return normalized path
    return str(Path(path).as_posix()).replace("\\", "/")


class MinioController:
    """Handler class for Minio operations.

    Attributes:
        logger (logging.Logger): Logger for this class.
        client (minio.Minio): Minio client.

    Methods:
        _upload (self, bucket: str, local_path: str, remote_path: str): Handles uploading a single file or directory recursively.
        _download (self, bucket: str, remote_path: str, local_path: str): Handles downloading a single file or directory recursively.
        _delete (self, bucket: str, remote_path: str): Deletes a single file or all files in a directory (prefix).
        upload (self, bucket: str, local_path: str, remote_path: str): Uploads a single file or directory recursively.
        download (self, bucket: str, remote_paths: t.Union[str, t.List[str]], local_path: str): Downloads one or more files/directories from MinIO.
        delete (self, bucket: str, remote_path: str): Deletes a single file or all files in a directory (prefix).
        exists (self, bucket: str, remote_path: str): Checks if a file or directory exists in MinIO.

    Raises:
        Exception: If there is an error connecting to MinIO.

    Example:
        controller = MinioController(endpoint="minio.example.com", access_key="minioaccesskey", secret_key="miniosecretkey", secure=True, cert_check=True)
        controller.upload("mybucket", "/path/to/local/file", "/path/to/remote/file")

    """

    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        secure: bool,
        cert_check: bool,
    ) -> None:
        ## Initialize class logger
        self.logger = log.getChild("MinioController")

        try:
            self.client = Minio(
                endpoint,
                access_key=access_key,
                secret_key=secret_key,
                secure=secure,
                cert_check=cert_check,
            )
        except Exception as exc:
            self.logger.error(f"Error connecting to minio: {exc}")
            raise

    def _upload(self, bucket: str, local_path: str, remote_path: str) -> None:
        """Handles uploading a single file or directory recursively.

        Params:
            bucket (str): Bucket name.
            local_path (str): Local path to file or directory.
            remote_path (str): Remote path to file or directory.

        Raises:
            FileNotFoundError: If local_path does not exist or is not a file/directory.

        Returns:
            None

        """
        if not self.client.bucket_exists(bucket):
            self.client.make_bucket(bucket)

        ## Replace any \ or \\ with /
        remote_path = normalize_path(remote_path)

        if Path(local_path).is_file():
            ## Path is file, upload single object
            self.logger.debug(
                f"Uploading file '{local_path}' to '{remote_path}' in bucket '{bucket}'"
            )
            try:
                self.client.fput_object(bucket, remote_path, local_path)
                self.logger.debug(
                    f"Uploaded '{local_path}' to '{remote_path}' in bucket '{bucket}'"
                )
            except Exception as exc:
                self.logger.error(
                    f"Error uploading '{local_path}' to '{remote_path}' in bucket '{bucket}': {exc}"
                )
                raise

        elif Path(local_path).is_dir():
            ## Path is a directory, create path & upload all objects
            for local_file in glob.glob(local_path + "/**", recursive=True):

                if Path(local_file).is_file():
                    rel_path = Path(local_file).relative_to(local_path)
                    remote_file_path = (Path(remote_path) / rel_path).as_posix()

                    self.logger.debug(
                        f"Uploading file '{local_file}' to '{remote_file_path}' in bucket '{bucket}'"
                    )
                    try:
                        self.client.fput_object(bucket, remote_file_path, local_file)
                        self.logger.debug(
                            f"Uploaded '{local_file}' to '{remote_file_path}' in bucket '{bucket}'"
                        )
                    except Exception as exc:
                        self.logger.error(
                            f"Error uploading '{local_file}' to '{remote_file_path}' in bucket '{bucket}': {exc}"
                        )
                        raise

        else:
            ## Path is not a file or directory
            raise FileNotFoundError(
                f"Local path '{local_path}' does not exist or is not a file/directory."
            )

    def _download(self, bucket: str, remote_path: str, local_path: str):
        """Handles downloading a single file or directory recursively.

        Params:
            bucket (str): Bucket name.
            remote_path (str): Remote path to file or directory.
            local_path (str): Local path to file or directory.

        Raises:
            FileNotFoundError: If remote_path does not exist or is not a file/directory.

        Returns:
            None

        """
        ## Replace any \ or \\ with /
        remote_path = normalize_path(remote_path)
        local_path = Path(local_path)

        ## Check if remote_path is a directory (prefix) or file
        if remote_path.endswith("/"):
            prefix = remote_path
            objects = self.client.list_objects(bucket, prefix=prefix, recursive=True)

            for obj in objects:
                rel_path = Path(obj.object_name).relative_to(prefix)
                local_file = local_path / rel_path
                local_file.parent.mkdir(parents=True, exist_ok=True)

                self.logger.debug(f"Downloading '{obj.object_name}' to '{local_file}'")
                self.client.fget_object(bucket, obj.object_name, str(local_file))
        else:
            ## Try to stat object to ensure it exists and is a file
            try:
                self.client.stat_object(bucket, remote_path)
            except S3Error as e:
                if e.code == "NoSuchKey":
                    raise FileNotFoundError(
                        f"Remote object '{remote_path}' not found in bucket '{bucket}'"
                    )
                raise

            local_path.parent.mkdir(parents=True, exist_ok=True)

            self.logger.debug(f"Downloading '{remote_path}' to '{local_path}'")
            self.client.fget_object(bucket, remote_path, str(local_path))

    def _copy(
        self, bucket: str, src_path: str, dest_path: str, dest_bucket: str | None = None
    ):
        """Copies a file or directory (prefix) from one location to another within MinIO.

        Params:
            bucket (str): Bucket name.
            src_path (str): Source path to file or directory.
            dest_path (str): Destination path to file or directory.
            dest_bucket (str, optional): Destination bucket name. Defaults to None.

        Raises:
            ValueError: If no remote paths are provided.

        Returns:
            None

        """
        src_path = normalize_path(src_path)
        dest_path = normalize_path(dest_path)
        dest_bucket = dest_bucket or bucket

        try:
            ## Use stat_object to check if the source exists and is a file.
            try:
                self.client.stat_object(bucket, src_path)
                ## It's a file, copy the file
                copy_source = CopySource(bucket, src_path)
                log.debug(
                    f"Copying object '{src_path}' from bucket '{bucket}' to '{dest_path}' in bucket '{dest_bucket}'"
                )
                self.client.copy_object(dest_bucket, dest_path, copy_source)

            except S3Error as e:
                if e.code == "NoSuchKey":
                    ## It might be a directory, list objects with the src_path as a prefix
                    objects = list(
                        self.client.list_objects(
                            bucket, prefix=src_path, recursive=True
                        )
                    )
                    if objects:
                        ## It's a directory (prefix), copy all objects under the prefix
                        for obj in objects:
                            ## Calculate the relative path within the source directory
                            #  Ensure no leading slash
                            rel_path = obj.object_name[len(src_path) :].lstrip("/")
                            #  Correctly join paths
                            new_dest_path = f"{dest_path.rstrip('/')}/{rel_path}"
                            copy_source = CopySource(bucket, obj.object_name)
                            log.debug(
                                f"Copying object '{obj.object_name}' from bucket '{bucket}' to '{new_dest_path}' in bucket '{dest_bucket}'"
                            )
                            self.client.copy_object(
                                dest_bucket, new_dest_path, copy_source
                            )
                    else:
                        ## No such key or directory
                        raise FileNotFoundError(
                            f"Source path '{src_path}' not found in bucket '{bucket}'."
                        ) from e
                else:
                    ## Re-raise the S3Error if it's not a NoSuchKey error
                    raise

        except Exception as exc:
            self.logger.error(
                f"Error copying '{src_path}' from bucket '{bucket}' to '{dest_path}' in bucket '{dest_bucket}': {exc}"
            )
            raise

    def _delete(self, bucket: str, remote_path: str):
        """Deletes a single object or all objects under a prefix (simulated directory).

        Params:
            bucket (str): Bucket name.
            remote_path (str): Remote path to file or directory.

        Raises:
            ValueError: If bucket does not exist.

        Returns:
            None

        """
        remote_path = normalize_path(remote_path).rstrip("/")

        if not self.client.bucket_exists(bucket):
            raise ValueError(f"Bucket '{bucket}' does not exist.")

        ## Check if it's a "directory" (prefix)
        prefix = remote_path + "/"
        objects = list(self.client.list_objects(bucket, prefix=prefix, recursive=True))

        if objects:
            delete_objects = [DeleteObject(obj.object_name) for obj in objects]

            self.logger.debug(
                f"Deleting [{len(delete_objects)}] object(s) under prefix '{prefix}'"
            )
            try:
                for error in self.client.remove_objects(bucket, delete_objects):
                    self.logger.error(
                        f"Error deleting object '{error.object_name}': {error}"
                    )
            except Exception as exc:
                self.logger.error(f"Failed to delete objects under '{prefix}': {exc}")
                raise
            return

        ## If not a prefix, try deleting as a single file
        try:
            self.client.remove_object(bucket, remote_path)
            self.logger.debug(
                f"Deleted single object '{remote_path}' from bucket '{bucket}'"
            )
        except S3Error as e:
            if e.code == "NoSuchKey":
                self.logger.warning(
                    f"Object '{remote_path}' not found in bucket '{bucket}'"
                )
            else:
                self.logger.error(
                    f"Error deleting '{remote_path}' from bucket '{bucket}': {e}"
                )
                raise
        except Exception as exc:
            self.logger.error(
                f"Error deleting '{remote_path}' from bucket '{bucket}': {exc}"
            )
            raise

    def upload(
        self, bucket: str, local_paths: t.Union[str, t.List[str]], remote_path: str = ""
    ):
        """Uploads one or more files/directories to MinIO."""
        if isinstance(local_paths, str):
            ## Replace any \ or \\ with /
            local_paths = [normalize_path(local_paths)]

        ## Replace any \ or \\ with /
        remote_path = normalize_path(remote_path)

        for path in local_paths:
            base_name = Path(path).name
            if remote_path:
                dest_path = (Path(remote_path) / base_name).as_posix()
            else:
                dest_path = base_name

            self._upload(bucket, path, dest_path)

    def download(
        self, bucket: str, remote_paths: t.Union[str, t.List[str]], local_path: str
    ):
        """Downloads one or more files/directories from MinIO."""
        if isinstance(remote_paths, str):
            ## Replace any \ or \\ with /
            remote_paths = [normalize_path(remote_paths)]

        for remote_path in remote_paths:
            ## Replace any \ or \\ with /
            remote_path = normalize_path(remote_path)
            self._download(bucket, remote_path, local_path)

    def object_exists(self, bucket: str, remote_path: str) -> bool:
        """Checks if a file or directory exists in MinIO.

        Params:
            bucket (str): Bucket name.
            remote_path (str): Remote path to file or directory.

        Returns:
            bool

        """
        remote_path = normalize_path(remote_path).rstrip("/")

        try:
            self.client.stat_object(bucket, remote_path)
            return True
        except S3Error as e:
            if e.code == "NoSuchKey":
                ## Could be a prefix/folder — let's check with list_objects
                prefix = remote_path + "/"
                objs = list(
                    self.client.list_objects(bucket, prefix=prefix, recursive=True)
                )
                return len(objs) > 0
            elif e.code == "AccessDenied":
                self.logger.error(
                    f"Access denied when checking object: {bucket}/{remote_path}"
                )
                raise
            else:
                raise

    def search_files(self, bucket: str, prefix: str) -> t.List[str]:
        """Searches a MinIO bucket for files with a given prefix.

        Params:
            bucket (str): Bucket name.
            prefix (str): Prefix to search for.

        Returns:
            List[str]

        """
        self.logger.debug(
            f"Searching minio bucket '{bucket}' for files with prefix '{prefix}'"
        )

        try:
            results = [
                obj.object_name
                for obj in self.client.list_objects(
                    bucket, prefix=prefix, recursive=True
                )
            ]
            self.logger.debug(
                f"Found [{len(results)}] file(s) with prefix '{prefix}' in minio bucket '{bucket}'"
            )

            return results
        except Exception as exc:
            self.logger.error(
                f"Error searching minio bucket '{bucket}' for files with prefix '{prefix}': {exc}"
            )
            raise

    def copy(
        self, bucket: str, src_path: str, dest_path: str, dest_bucket: str | None = None
    ):
        """Copies a file or directory (prefix) from one location to another within MinIO.

        Params:
            bucket (str): Bucket name.
            src_path (str): Source path to file or directory.
            dest_path (str): Destination path to file or directory.
            dest_bucket (str | None, optional): Destination bucket name. Defaults to None.

        Raises:
            ValueError: If bucket does not exist.

        Returns:
            None

        """
        try:
            self._copy(bucket, src_path, dest_path, dest_bucket)
        except Exception as e:
            self.logger.error(f"Failed to copy {src_path} to {dest_path}: {e}")
            raise

    def move(
        self, bucket: str, src_path: str, dest_path: str, dest_bucket: str | None = None
    ):
        """Moves a file or directory from one location to another within MinIO.

        Params:
            bucket (str): Bucket name.
            src_path (str): Source path to file or directory.
            dest_path (str): Destination path to file or directory.
            dest_bucket (str | None, optional): Destination bucket name. Defaults to None.

        Raises:
            ValueError: If bucket does not exist.

        Returns:
            None

        """
        src_path = normalize_path(src_path)
        dest_path = normalize_path(dest_path)
        dest_bucket = dest_bucket or bucket

        try:
            ## Copy the object(s) first
            self._copy(bucket, src_path, dest_path, dest_bucket)

            ## Determine if we are moving a single file or a directory (prefix)
            try:
                self.client.stat_object(bucket, src_path)
                ## It's a file, remove the single file
                self.client.remove_object(bucket, src_path)
                log.debug(f"Removed object '{src_path}' from bucket '{bucket}'")

            except S3Error as e:
                if e.code == "NoSuchKey":
                    ## It must be a directory, remove all objects under the prefix
                    objects = list(
                        self.client.list_objects(
                            bucket, prefix=src_path, recursive=True
                        )
                    )
                    if objects:
                        for obj in objects:
                            self.client.remove_object(bucket, obj.object_name)
                            log.debug(
                                f"Removed object '{obj.object_name}' from bucket '{bucket}'"
                            )
                    else:
                        raise FileNotFoundError(
                            f"Source path '{src_path}' not found in bucket '{bucket}'."
                        ) from e
                else:
                    ## Re-raise the S3Error if it's not a NoSuchKey error
                    raise

        except Exception as exc:
            self.logger.error(
                f"Error moving '{src_path}' from bucket '{bucket}' to '{dest_path}' in bucket '{dest_bucket}': {exc}"
            )
            raise

    def delete(self, bucket: str, remote_paths: t.Union[str, t.List[str]]):
        """Deletes one or more files/directories from MinIO.

        Params:
            bucket (str): Bucket name.
            remote_path (str): Remote path to file or directory.

        Raises:
            ValueError: If no remote paths are provided.

        Returns:

        """
        if not remote_paths:
            raise ValueError("No remote paths provided to delete.")

        if isinstance(remote_paths, str):
            ## Replace any \ or \\ with /
            remote_paths = [remote_paths]

        for remote_path in remote_paths:
            ## Replace any \ or \\ with /
            remote_path = normalize_path(remote_path)
            self._delete(bucket, remote_path)


if __name__ == "__main__":
    """If the script is called directly, initialize a MinioController and run the CLI."""
    import argparse
    import json
    import logging

    args = parse_args()

    ## Configure logging
    logging.basicConfig(
        level="DEBUG" if args.debug else "INFO",
        format=(
            "%(asctime)s | [%(levelname)s] | %(name)s:%(lineno)s :: %(message)s"
            if args.debug
            else "%(asctime)s [%(levelname)s] :: %(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    for _logger in ["urllib3"]:
        logging.getLogger("urllib3").disabled = True

    if args.generate_configs:
        try:
            generate_default_configs()
            exit(0)
        except Exception as exc:
            log.error(exc)
            exit(1)

    ## Load MinIO configuration
    if args.minio_config and Path(args.minio_config).exists():
        with open(args.minio_config, "r") as f:
            minio_config = json.load(f)
    elif args.minio_config and not Path(args.minio_config).exists():
        log.warning(
            f"Minio config file not found at path '{args.minio_config}'. Generating default config"
        )
        generated_config = MinioConfigGenerator()
        generated_config.generate()

    endpoint = args.minio_endpoint or minio_config.get("endpoint")
    access_key = args.minio_access_key or minio_config.get("access_key")
    secret_key = args.minio_secret_key or minio_config.get("secret_key")
    secure = args.secure or minio_config.get("secure")
    cert_check = args.check_cert or minio_config.get("cert_check")

    if not all([endpoint, access_key, secret_key]):
        log.error(
            "Missing MinIO configuration.  Please provide endpoint, access_key, and secret_key via command line or minio_config.json."
        )
        exit(1)

    ## Initialize MinIO Controller
    controller = get_minio_controller(
        endpoint, access_key, secret_key, secure=secure, cert_check=cert_check
    )

    ## Handle job file
    if args.job_file:
        try:
            job = load_minio_job(args.job_file)

            if isinstance(job, MinioUploadJob):
                controller.upload(job.bucket, job.local_path, job.remote_path)
            elif isinstance(job, MinioDownloadJob):
                controller.download(job.bucket, job.remote_path, job.local_path)
            elif isinstance(job, MinioDeleteJob):
                controller.delete(job.bucket, job.remote_path)
            elif isinstance(job, MinioCopyJob):
                controller.copy(
                    bucket=job.bucket,
                    src_path=job.remote_path,
                    dest_path=job.remote_dest,
                    dest_bucket=job.dest_bucket,
                )
            elif isinstance(job, MinioMoveJob):
                controller.move(
                    bucket=job.bucket,
                    src_path=job.remote_path,
                    dest_path=job.remote_dest,
                    dest_bucket=job.dest_bucket,
                )

            log.info(f"Job '{args.job_file}' completed successfully.")

        except Exception as e:
            log.error(f"Error processing job file '{args.job_file}': {e}")
            exit(0)

        log.info("Job completed successfully.")
    else:
        log.error("No job file provided.")
        exit(1)

```
