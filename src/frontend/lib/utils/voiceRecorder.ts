/**
 * Voice Recorder utility for Web Audio API
 * Captures audio for voice baseline establishment
 */

export class VoiceRecorder {
    private mediaRecorder: MediaRecorder | null = null;
    private audioChunks: Blob[] = [];
    private stream: MediaStream | null = null;
    private audioContext: AudioContext | null = null;
    private analyser: AnalyserNode | null = null;
    private dataArray: Uint8Array | null = null;

    /**
     * Initialize the audio recorder
     */
    async init(): Promise<void> {
        try {
            // Request microphone access
            this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });

            // Create audio context for visualization
            this.audioContext = new AudioContext({ sampleRate: 24000 });
            this.analyser = this.audioContext.createAnalyser();
            this.analyser.fftSize = 256;

            const bufferLength = this.analyser.frequencyBinCount;
            this.dataArray = new Uint8Array(bufferLength);

            const source = this.audioContext.createMediaStreamSource(this.stream);
            source.connect(this.analyser);

            // Create MediaRecorder
            this.mediaRecorder = new MediaRecorder(this.stream, {
                mimeType: 'audio/webm;codecs=opus'
            });

            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.audioChunks.push(event.data);
                }
            };

        } catch (error) {
            console.error('Failed to initialize audio recorder:', error);
            throw new Error('Microphone access denied');
        }
    }

    /**
     * Start recording
     */
    start(): void {
        if (!this.mediaRecorder) {
            throw new Error('Recorder not initialized');
        }

        this.audioChunks = [];
        this.mediaRecorder.start(100); // Collect data every 100ms
    }

    /**
     * Stop recording and return audio blob
     */
    async stop(): Promise<Blob> {
        return new Promise((resolve, reject) => {
            if (!this.mediaRecorder) {
                reject(new Error('Recorder not initialized'));
                return;
            }

            this.mediaRecorder.onstop = () => {
                const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
                resolve(audioBlob);
            };

            this.mediaRecorder.stop();
        });
    }

    /**
     * Get current audio level for visualization (0-255)
     */
    getAudioLevel(): number {
        if (!this.analyser || !this.dataArray) {
            return 0;
        }

        this.analyser.getByteFrequencyData(this.dataArray);

        // Calculate average amplitude
        const average = this.dataArray.reduce((sum, value) => sum + value, 0) / this.dataArray.length;
        return average;
    }

    /**
     * Get frequency data for waveform visualization
     */
    getFrequencyData(): Uint8Array {
        if (!this.analyser || !this.dataArray) {
            return new Uint8Array(0);
        }

        this.analyser.getByteFrequencyData(this.dataArray);
        return new Uint8Array(this.dataArray);
    }

    /**
     * Convert audio blob to base64 for API transmission
     */
    async blobToBase64(blob: Blob): Promise<string> {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onloadend = () => {
                const base64 = (reader.result as string).split(',')[1];
                resolve(base64);
            };
            reader.onerror = reject;
            reader.readAsDataURL(blob);
        });
    }

    /**
     * Convert audio blob to Float32Array for processing
     */
    async blobToFloat32Array(blob: Blob): Promise<Float32Array> {
        const arrayBuffer = await blob.arrayBuffer();

        if (!this.audioContext) {
            throw new Error('Audio context not initialized');
        }

        const audioBuffer = await this.audioContext.decodeAudioData(arrayBuffer);
        return audioBuffer.getChannelData(0); // Mono audio
    }

    /**
     * Clean up resources
     */
    cleanup(): void {
        if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
            this.mediaRecorder.stop();
        }

        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
        }

        if (this.audioContext && this.audioContext.state !== 'closed') {
            this.audioContext.close();
        }

        this.mediaRecorder = null;
        this.stream = null;
        this.audioContext = null;
        this.analyser = null;
        this.dataArray = null;
        this.audioChunks = [];
    }
}

/**
 * Check if browser supports required audio features
 */
export function isAudioSupported(): boolean {
    return !!(
        navigator.mediaDevices &&
        navigator.mediaDevices.getUserMedia &&
        window.AudioContext
    );
}

/**
 * Request microphone permission
 */
export async function requestMicrophonePermission(): Promise<boolean> {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        stream.getTracks().forEach(track => track.stop());
        return true;
    } catch (error) {
        console.error('Microphone permission denied:', error);
        return false;
    }
}
