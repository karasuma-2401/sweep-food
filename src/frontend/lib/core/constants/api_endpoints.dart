class ApiEndpoints {
  static const String baseUrl = 'http://10.0.2.2:8000/api/v1'; // 10.0.2.2 cho Android Emulator

  // Ingestion AI Endpoints
  static const String scanReceipt = '/ingestion/ocr/receipt';
  static const String scanLabel = '/ingestion/ocr/label';
  static const String detectFreshFood = '/ingestion/vision/detect';
  static const String transcribeVoice = '/ingestion/voice/transcribe';

  // Pantry & Recommendation
  static const String pantryItems = '/pantry/items';
  static const String recommendRecipes = '/recipes/recommend';
}