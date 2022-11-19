/*******************************************************************************
 * DJ Joe Playlister Build Automation
 *
 * Build, Deploy, and Share the Playlist Generator
 ******************************************************************************/

node ('djjoeappserv') {

    // Build in the DJ Joe Application Server
    checkout scm

    testPython()

    buildContainer()

}


// Test Python Scripts
def testPython() {
    stage("Test Python") {
        // Install Python Requirements
        sh "python3 -m pip install --upgrade --no-cache-dir -r app/requirements.txt"
        sh "python3 -m pip install --upgrade --no-cache-dir -r test/pytest-requires.txt"

        // Run Tests
        sh "python3 -m pytest"
    }
}


// Build the Application
def buildContainer() {
    stage("Build Container") {
        //sh "docker build "
    }
}