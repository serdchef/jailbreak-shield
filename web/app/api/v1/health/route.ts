import { NextResponse } from 'next/server';

export async function GET() {
    return NextResponse.json({
        status: 'healthy',
        engine: 'ready',
        version: '3.0.0'
    });
}
