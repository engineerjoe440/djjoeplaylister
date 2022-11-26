/*******************************************************************************
 * DJ Joe Playlister Build Automation
 *
 * Build, Deploy, and Share the Playlist Generator
 ******************************************************************************/

node ('x86-32-build') {

    // Build in the DJ Joe Application Server
    checkout scm

    // Provide Credentials to Support Spotify Client
    withCredentials([
            usernamePassword(credentialsId: 'SPOTIFY_ID_AND_KEY',
            usernameVariable: 'SPOTIFY_ID',
            passwordVariable: 'SPOTIFY_SECRET')
        ]) {

        testPython()

        buildContainer()

        pushContainer()
    }

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
        sh "docker build -t engineerjoe440/playlist-generator:latest ."
    }
}


// Push the Application Container to Docker-Hub
def pushContainer() {
    stage("Push Container") {
        sh "docker push engineerjoe440/playlist-generator:latest"
    }
}