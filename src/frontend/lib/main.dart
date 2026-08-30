import 'package:flutter/material.dart';
import 'app/routes/app_pages.dart';
import 'injection_container.dart' as di;

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await di.initDependencies();
  runApp(const SweepFoodApp());
}

class SweepFoodApp extends StatelessWidget {
  const SweepFoodApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'SweepFood',
      debugShowCheckedModeBanner: false,
      routerConfig: AppPages.router,
      theme: ThemeData(
        useMaterial3: true,
        colorSchemeSeed: const Color(0xFF2E7D32),
      ),
    );
  }
}
