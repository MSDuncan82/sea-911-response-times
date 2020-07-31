import dotenv
import boto3
import os
import shutil
import uuid


class S3Exec:
    """
    TODO Write class docs
    short description of class
    
    longer description of class if necessary
    
    Attributes
    ----------
    attribute : type
        attribute description
    
    Methods
    ---------
    method(*args, **kwargs)
        method description
    """
    

    def __init__(self, find_creds=True, **kwargs):
        """
        Initiate boto connection to S3
        """

        if find_creds:
            dotenv.load_dotenv()
            creds = self.find_creds()
            kwargs = creds

        self.session = boto3.session.Session(**kwargs)
        self.s3_client = self.session.client("s3")
        self.s3_resource = self.session.resource("s3")

    def find_creds(self):
        """
        Find credentials from environment variables
        """

        creds = {}
        creds['aws_access_key_id'] = os.environ['AWSAccessKeyId']
        creds['aws_secret_access_key'] = os.environ['AWSSecretKey']
        return creds

    def search_files(self, file_str, ):
        """
        Search all files in all buckets and return matches in a dict {'bucket name': 'file key'}
        """

        buckets = self.list_buckets()
        file_matches = {}
        for bucket in buckets:
            files = self.list_files(bucket.name)
            if files:
                for file in files:
                    if file_str in file.key:
                        file_matches[bucket] = file

        return file_matches

    def download_file_match(self, file_str, file_outpath, overwrite=False):
        """
        Search all files in all buckets and download matching file using `file_str`
        """

        file_matches = self.search_files(file_str)

        bucket, file = self.check_matches(file_matches, file_str)

        self.download_file(file_outpath, bucket, file, overwrite=overwrite)

    def download_file(self, file_outpath, bucket, file, overwrite=False):
        """
        Download a specific file with input bucket object & file object
        """

        check_file_outpath = not os.path.exists(file_outpath)

        if check_file_outpath or overwrite:
            with open(file_outpath, 'wb+') as file_out:
                self.s3_client.download_fileobj(bucket.name, file.key, file_out)
        else:
            raise FileExistsError('File already exists. Use `overwrite=True` to overwrite the file')
    
    def check_matches(self, file_matches, file_str):
        """
        check that only 1 match exists and return it
        """

        if len(file_matches) > 1:
            raise FileExistsError(f'More than one file with {file_str} found')
        elif len(file_matches) == 0:
            raise FileNotFoundError(f'No file found that matches {file_str}')
        else:
            bucket, file = next(iter(file_matches.items()))

        return bucket, file

    def list_buckets(self):
        """
        Return list of s3 buckets
        """

        return list(self.s3_resource.buckets.all())

    def list_files(self, bucket):
        """
        Return list of file objects in a given s3 bucket
        """
        try:
            return list(self.s3_resource.Bucket(bucket).objects.all())
        except Exception as e:
            print(f'Caught exception {e} for {bucket}')

    def create_bucket_name(self, bucket_prefix):
        """
        The generated bucket name must be between 3 and 63 chars long
        """

        return "".join([bucket_prefix, str(uuid.uuid4())])

    def create_bucket(self, bucket_prefix, s3_connection, versioning=True):
        """
        Create bucket with unique name
        """

        if s3_connection is None:
            s3_connection = self.s3_resource

        current_region = self.session.region_name
        bucket_name = self.create_bucket_name(bucket_prefix)

        bucket_response = s3_connection.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": current_region},
        )

        if versioning:
            bkt_versioning = self.s3_resource.BucketVersioning(bucket_name)
            bkt_versioning.enable()

        return bucket_name, bucket_response

    def generate_random_filename(self, filename):
        """
        Generate filename with random prefix
        """

        return "".join([str(uuid.uuid4().hex[:6]), f"_{filename}"])

    def rename_existing_files(self, filepath):
        """
        Remame existing file
        """

        filename = os.path.basename(filepath).split(".")[0]
        filedir = os.path.join(*filepath.split("/")[:-1])
        random_file_name = self.generate_random_filename(filename)
        os.rename(filepath, f"{filedir}/{random_file_name}.csv")

    def delete_object(self, bucket, file):
        """
        Delete a file in a given bucket by substring
        """
        pass

    def delete_all_objects(self, bucket):
        """Delete all objects in bucket"""

        res = []
        for obj_version in bucket.object_versions.all():
            res.append({"Key": obj_version.object_key, "VersionId": obj_version.id})

        bucket.delete_objects(Delete={"Objects": res})


if __name__ == "__main__":

    s3_exec = S3Exec()
