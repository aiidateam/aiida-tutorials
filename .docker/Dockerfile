FROM aiidateam/aiida-core:stable

COPY aiida-environment.yml /tmp/aiida-environment.yml

RUN conda env update --name root --file /tmp/aiida-environment.yml

COPY import-aiida-archive.sh /opt/import-aiida-archive.sh
COPY run-import-aiida-archive.sh /etc/my_init.d/50_import-aiida-archive.sh

WORKDIR /tmp/mount_folder/
