import axios, { AxiosInstance } from 'axios';

export interface ShieldConfig {
    baseUrl?: string;
    apiKey?: string;
}

export interface ShieldAnalysis {
    safe: boolean;
    risk_score: number;
    attack_detected: boolean;
    attack_type?: string;
    primary_layer: string;
    explanation: string;
}

export class AegisClient {
    private client: AxiosInstance;

    constructor(config: ShieldConfig = {}) {
        this.client = axios.create({
            baseURL: config.baseUrl || 'http://localhost:8000/api/v1',
            headers: config.apiKey ? { 'Authorization': `Bearer ${config.apiKey}` } : {}
        });
    }

    async analyze(prompt: string, userId: string = 'anonymous'): Promise<ShieldAnalysis> {
        try {
            const response = await this.client.post('/analyze', {
                prompt,
                user_id: userId
            });
            return response.data;
        } catch (error) {
            console.error('Shield Analysis Failed:', error);
            throw error;
        }
    }
}
