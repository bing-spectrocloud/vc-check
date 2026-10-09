import os
import ssl
from pyVim.connect import SmartConnectNoSSL, Disconnect

def test_vcenter_connection():
    # 1. Gather env variables set by the GitHub Action workflow
    host = os.getenv("VCENTER_HOST", "localhost")
    port = int(os.getenv("VCENTER_PORT", 8989))
    user = os.getenv("VCENTER_USER", "user")
    password = os.getenv("VCENTER_PASS", "pass")

    # 2. CRITICAL: Create an unverified SSL context to bypass self-signed cert issues
    context = ssl._create_unverified_context()

    try:
        # 3. Connect to the simulator
        si = SmartConnectNoSSL(
            host=host,
            user=user,
            pwd=password,
            port=port,
            sslContext=context
        )

        # 4. Verify connectivity by retrieving the root folder name
        content = si.RetrieveContent()
        root_folder = content.rootFolder

        assert root_folder is not None
        print(f"Successfully connected to vcsim root folder: {root_folder.name}")

    finally:
        # Clean up connection
        if 'si' in locals():
            Disconnect(si)

if __name__ == '__main__':
    test_vcenter_connection()
