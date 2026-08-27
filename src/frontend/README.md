# SweepFood Frontend

Ứng dụng Flutter đa nền tảng cho SweepFood — sản phẩm hỗ trợ quản lý thực phẩm và gợi ý công thức.

> **Trạng thái hiện tại:** repository mới chứa Flutter scaffold và danh sách dependency; chưa có thư mục `lib/` hay luồng nghiệp vụ. Các phần kiến trúc bên dưới là quy ước triển khai để cả team bắt đầu thống nhất, không phải các tính năng đã hoàn thành.

## Công nghệ

| Nhóm | Thư viện / công cụ |
| --- | --- |
| Framework | Flutter / Dart (Dart SDK `^3.5.0`) |
| Quản lý trạng thái | `flutter_bloc`, `equatable` |
| Dependency injection | `get_it` |
| Điều hướng | `go_router` |
| HTTP | `dio` |
| Lưu trữ cục bộ | `shared_preferences`, `flutter_secure_storage` |
| Ảnh, biểu đồ và giao diện | `image_picker`, `image_cropper`, `flutter_svg`, `cached_network_image`, `fl_chart`, `intl` |

Ứng dụng đã được tạo cho Android, iOS, Web, Windows, macOS và Linux. Khi phát triển tính năng mới, ưu tiên kiểm tra trên Android và Web; các nền tảng còn lại chỉ bật khi được yêu cầu.

## Yêu cầu môi trường

- Flutter SDK tương thích với Dart `^3.5.0` (kiểm tra bằng `flutter --version`).
- Android Studio + Android SDK để chạy Android; Xcode chỉ cần khi build iOS/macOS trên macOS.
- Thiết bị thật hoặc emulator/simulator đã khởi động.

Kiểm tra toàn bộ môi trường trước khi bắt đầu:

```powershell
flutter doctor
```

## Cài đặt và chạy local

Từ thư mục gốc repository:

```powershell
cd src/frontend
flutter pub get
flutter devices
flutter run
```

Chạy cho một nền tảng cụ thể:

```powershell
flutter run -d chrome
flutter run -d windows
flutter run -d <device-id>
```

Lần đầu chạy Android có thể cần chấp nhận Android SDK licenses:

```powershell
flutter doctor --android-licenses
```

## Kiểm tra trước khi tạo pull request

```powershell
cd src/frontend
flutter format .
flutter analyze
flutter test
```

`test/widget_test.dart` hiện vẫn là smoke test mặc định của Flutter và tham chiếu `lib/main.dart`, trong khi `lib/` chưa được thêm. Hãy thay test này cùng lúc khi tạo điểm vào ứng dụng đầu tiên; khi đó `flutter test` mới là kiểm tra có ý nghĩa.

## Quy ước cấu trúc đề xuất

Khi bắt đầu triển khai, tạo cấu trúc dưới đây để tách giao diện khỏi dữ liệu và nghiệp vụ:

```text
lib/
├── app/
│   ├── app.dart                 # MaterialApp.router, theme
│   ├── router/                  # Khai báo GoRouter và guard
│   └── di/                      # Đăng ký GetIt
├── core/
│   ├── network/                 # Dio, interceptor, API errors
│   ├── storage/                 # Secure/local storage wrappers
│   ├── constants/
│   └── widgets/                 # Widget dùng chung
├── features/
│   └── <feature>/
│       ├── data/                # DTO, datasource, repository implementation
│       ├── domain/              # Entity, repository contract, use case (nếu cần)
│       └── presentation/        # Page, widget, Bloc/Cubit
└── main.dart                    # Bootstrap và gọi configureDependencies()
assets/
├── images/
└── icons/
```

Một feature chỉ được truy cập API qua repository. Page/widget giao tiếp với `Bloc`/`Cubit`, không gọi `Dio` hoặc `shared_preferences` trực tiếp. Đăng ký các service và repository vào GetIt tại `lib/app/di/` để dễ mock khi test.

## Cấu hình API và dữ liệu nhạy cảm

Chưa có endpoint hoặc cơ chế cấu hình API được commit. Khi bổ sung, truyền base URL lúc chạy thay vì hard-code:

```powershell
flutter run --dart-define=API_BASE_URL=https://api.example.com
```

Đọc giá trị tại một chỗ duy nhất, ví dụ `const String.fromEnvironment('API_BASE_URL')`, rồi cấp cho `Dio`. Không commit token, khóa API, keystore hoặc tệp `.env`; `.env` đã nằm trong `.gitignore`. Token đăng nhập phải lưu bằng `flutter_secure_storage`, không dùng `shared_preferences`.

## Quy ước phát triển

- Tên file dùng `snake_case`; class/widget dùng `PascalCase`; biến và method dùng `camelCase`.
- Ưu tiên `const` widget và các component nhỏ, tái sử dụng được.
- Mỗi trạng thái tải/rỗng/lỗi của màn hình phải được thiết kế rõ ràng.
- DTO từ API không truyền thẳng vào UI; map về model/entity của feature.
- Thêm test cho Bloc/Cubit, mapper và widget quan trọng cùng với feature.
- Cập nhật `pubspec.yaml` và chạy `flutter pub get` khi thêm dependency để lockfile được đồng bộ.

## Build phát hành

Xác nhận kiểm tra chất lượng đã pass rồi chạy một trong các lệnh sau:

```powershell
# Android APK (sideload / internal testing)
flutter build apk --release

# Android App Bundle (Google Play)
flutter build appbundle --release

# Web
flutter build web --release

# Windows
flutter build windows --release
```

Artifact được tạo trong `build/` và không được commit. Trước khi phát hành Android, thay `applicationId` mặc định `com.example.frontend`, nhãn app và cấu hình ký release trong `android/app/build.gradle.kts`. Trước khi phát hành web, cập nhật tên, mô tả, màu chủ đạo và icon trong `web/manifest.json`.

## Tài liệu liên quan

- [Yêu cầu sản phẩm](../../docs/requirement.md)
- [Backend](../backend/README.md)
