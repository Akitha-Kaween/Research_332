
import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  // Use localhost for iOS simulator, 10.0.2.2 for Android Emulator
  final Dio _dio = Dio(BaseOptions(baseUrl: 'http://localhost:8000'));
  String? _token;

  ApiService() {
    _loadToken();
  }

  Future<void> _loadToken() async {
    final prefs = await SharedPreferences.getInstance();
    _token = prefs.getString('auth_token');
    if (_token != null) {
      _dio.options.headers['Authorization'] = 'Bearer $_token';
    }
  }

  // --- Auth ---
  Future<bool> login(String email, String password) async {
    try {
      final response = await _dio.post('/auth/login', data: {
        'username': email,
        'password': password,
      }, options: Options(contentType: Headers.formUrlEncodedContentType));
      
      _token = response.data['access_token'];
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('auth_token', _token!);
      _dio.options.headers['Authorization'] = 'Bearer $_token';
      return true;
    } catch (e) {
      print('Login Error: $e');
      return false;
    }
  }

  Future<bool> register(String name, String email, String password) async {
    try {
      await _dio.post('/auth/register', data: {
        'email': email,
        'password': password,
        'name': name
      });
      return true;
    } catch (e) {
      print('Register Error: $e');
      return false;
    }
  }

  // --- Component 1: Crowd ---
  Future<Map<String, dynamic>> getCrowdPrediction(String location, String date) async {
    try {
      final response = await _dio.post('/crowd/api/predict', data: {
        'location': location,
        'date': date,
        'time': '10:00'
      });
      return response.data;
    } catch (e) {
      print('Crowd Error: $e');
      return {'error': 'Failed to get crowd data'};
    }
  }

  // --- Component 2: Food ---
  Future<List<dynamic>> getFoodRecommendations(int userId) async {
    try {
      final response = await _dio.post('/food/api/recommend', data: {
        'user_id': userId,
        'n_recommendations': 5
      });
      return response.data['recommendations'];
    } catch (e) {
      print('Food Error: $e');
      return [];
    }
  }

  // --- Component 3: Travel Agent ---
  Future<Map<String, dynamic>> chatWithAgent(String message) async {
    try {
      final response = await _dio.post('/travel/agent/chat', data: {
        'message': message
      });
      return response.data;
    } catch (e) {
      print('Agent Error: $e');
      return {'response': 'Error connecting to Agent.', 'action_type': 'error'};
    }
  }
}
