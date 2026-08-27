import 'package:dio/dio.dart';
import '../constants/api_endpoints.dart';
import 'interceptors/auth_interceptor.dart';

class ApiClient {
  late final Dio dio;

  ApiClient() {
    dio = Dio(
      BaseOptions(
        baseUrl: ApiEndpoints.baseUrl,
        connectTimeout: const Duration(seconds: 30),
        receiveTimeout: const Duration(seconds: 30),
        headers: {'Content-Type': 'application/json'},
      ),
    );
    dio.interceptors.add(AuthInterceptor());
    dio.interceptors.add(LogInterceptor(responseBody: true, requestBody: true));
  }
}
