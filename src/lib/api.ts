/**
 * API client for periph4all backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface UserPreferences {
  hand_size?: string | null; // Accepts exact dimensions (e.g., "19cm x 10cm") or small/medium/large
  grip_type?: string | null; // palm, claw, fingertip, or hybrid
  genre?: string | null; // fps, moba, mmo, battle_royale, or general
  sensitivity?: string | null; // low, medium, high
  budget_min?: number | null;
  budget_max?: number | null;
  weight_preference?: string | null; // light, medium, heavy
  wireless_preference?: boolean | null;
  additional_notes?: string | null;
}

export interface ChatResponse {
  message: ChatMessage;
  updated_preferences?: UserPreferences;
  ready_for_recommendation: boolean;
  question_type?: string | null; // Type of question: hand_size, grip_type, genre, sensitivity, budget, weight_preference, wireless_preference
}

export interface MouseInfo {
  name: string;
  brand: string;
  price?: number;
  weight?: number;
  dpi_max?: number;
  wireless?: boolean;
  shape?: string;
  sensor?: string;
  url?: string;
}

export interface RecommendationItem {
  mouse: MouseInfo;
  score: number;
  reasoning: string;
}

export interface RecommendationsResponse {
  recommendations: RecommendationItem[];
  preferences_used: UserPreferences;
}

/**
 * Send a chat message and get AI response
 */
export async function sendChatMessage(
  messages: ChatMessage[],
  currentPreferences?: UserPreferences
): Promise<ChatResponse> {
  // Add timeout to prevent hanging
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 30000); // 30s timeout

  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/chat/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messages,
        current_preferences: currentPreferences || null,
      }),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  } catch (error) {
    clearTimeout(timeoutId);
    if (error instanceof Error && error.name === 'AbortError') {
      throw new Error('Request timed out. Please check if the backend is running.');
    }
    throw error;
  }
}

/**
 * Get mouse recommendations based on preferences
 */
export async function getRecommendations(
  preferences: UserPreferences
): Promise<RecommendationsResponse> {
  // Add timeout to prevent hanging
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 30000); // 30s timeout

  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/recommendations/quick`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(preferences),  // Send preferences directly, not wrapped
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  } catch (error) {
    clearTimeout(timeoutId);
    if (error instanceof Error && error.name === 'AbortError') {
      throw new Error('Request timed out. Please check if the backend is running.');
    }
    throw error;
  }
}

/**
 * Quick health check
 */
export async function healthCheck(): Promise<{ status: string }> {
  const response = await fetch(`${API_BASE_URL}/health`);
  
  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

/**
 * Visualization Types
 */
export interface EmbeddingPoint {
  x: number;
  y: number;
  mouse_name: string;
  mouse_info?: MouseInfo;
}

export interface VisualizationResponse {
  mouse_points: EmbeddingPoint[];
  user_point?: EmbeddingPoint;
  recommended_points?: EmbeddingPoint[];
}

/**
 * Get UMAP visualization data with user preferences
 */
export async function getVisualizationWithUser(
  preferences: UserPreferences
): Promise<VisualizationResponse> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 30000);

  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/visualizations/embedding-space-with-user`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(preferences),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  } catch (error) {
    clearTimeout(timeoutId);
    if (error instanceof Error && error.name === 'AbortError') {
      throw new Error('Request timed out. Please check if the backend is running.');
    }
    throw error;
  }
}

export interface GraphData {
  visualization: {
    mouse_points: EmbeddingPoint[];
    user_point: EmbeddingPoint | null;
    recommended_points: EmbeddingPoint[] | null;
  };
  edges: Array<{
    source: number;
    target: number;
    similarity: number;
  }>;
  user_edges: Array<{
    source: string;
    target: number;
    similarity: number;
  }>;
  k_neighbors: number;
}

export async function getGraphData(
  preferences: UserPreferences,
  kNeighbors: number = 5
): Promise<GraphData> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 30000);

  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/visualizations/graph-data?k_neighbors=${kNeighbors}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(preferences),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`Failed to fetch graph data: ${response.status}`);
    }

    return response.json();
  } catch (error) {
    clearTimeout(timeoutId);
    if (error instanceof Error && error.name === 'AbortError') {
      throw new Error('Request timed out. Please check if the backend is running.');
    }
    throw error;
  }
}
