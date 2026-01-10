
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/api_service.dart';
// import 'package:webview_flutter/webview_flutter.dart'; // For real map view

class TravelAgentScreen extends StatefulWidget {
  const TravelAgentScreen({super.key});

  @override
  State<TravelAgentScreen> createState() => _TravelAgentScreenState();
}

class _TravelAgentScreenState extends State<TravelAgentScreen> {
  final TextEditingController _controller = TextEditingController();
  final List<Map<String, dynamic>> _messages = []; // {text, isUser, type}
  bool _isLoading = false;

  void _sendMessage() async {
    if (_controller.text.isEmpty) return;
    
    final text = _controller.text;
    setState(() {
      _messages.add({'text': text, 'isUser': true});
      _isLoading = true;
    });
    _controller.clear();

    final api = Provider.of<ApiService>(context, listen: false);
    final response = await api.chatWithAgent(text);

    setState(() {
      _isLoading = false;
      _messages.add({
        'text': response['response'],
        'isUser': false,
        'type': response['action_type']
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('AI Travel Agent')),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final msg = _messages[index];
                final isUser = msg['isUser'];
                return Align(
                  alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    margin: const EdgeInsets.only(bottom: 12),
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                    decoration: BoxDecoration(
                      color: isUser ? const Color(0xFF00BFA5) : Colors.white,
                      borderRadius: BorderRadius.only(
                        topLeft: const Radius.circular(12),
                        topRight: const Radius.circular(12),
                        bottomLeft: isUser ? const Radius.circular(12) : Radius.zero,
                        bottomRight: isUser ? Radius.zero : const Radius.circular(12),
                      ),
                      boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 4)],
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          msg['text'],
                          style: TextStyle(color: isUser ? Colors.white : Colors.black87),
                        ),
                        if (msg['type'] == 'map')
                           Padding(
                             padding: const EdgeInsets.only(top: 8.0),
                             child: ElevatedButton.icon(
                               onPressed: () {
                                 Navigator.push(context, MaterialPageRoute(builder: (_) => const MapViewerScreen(url: 'http://localhost:8000/static/minimal_tour_map.html')));
                               },
                               icon: const Icon(Icons.map, size: 16),
                               label: const Text('View Route Map'),
                               style: ElevatedButton.styleFrom(
                                 backgroundColor: Colors.blueAccent, 
                                 foregroundColor: Colors.white,
                                 minimumSize: const Size(0, 36)
                               ),
                             ),
                           ),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
          if (_isLoading) const LinearProgressIndicator(backgroundColor: Colors.transparent),
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: InputDecoration(
                      hintText: 'Try "Optimize Kandy tour"...',
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(24)),
                      contentPadding: const EdgeInsets.symmetric(horizontal: 20),
                    ),
                    onSubmitted: (_) => _sendMessage(),
                  ),
                ),
                const SizedBox(width: 8),
                FloatingActionButton(
                  onPressed: _sendMessage,
                  mini: true,
                  backgroundColor: const Color(0xFF00BFA5),
                  child: const Icon(Icons.send, color: Colors.white),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class MapViewerScreen extends StatelessWidget {
  final String url;
  const MapViewerScreen({super.key, required this.url});

  @override
  Widget build(BuildContext context) {
    // Note: Use 10.0.2.2 for Android Emulator if testing there
    // For iOS Simulator, localhost is fine.
    
    // WebViewController setup would go here for webview_flutter 4.0+
    // For brevity, we assume standard usage.
    
    return Scaffold(
      appBar: AppBar(title: const Text('Optimized Route')),
        // Placeholder for WebView widget since API varies by version.
        // In real impl: WebViewWidget(controller: WebViewController()..loadRequest(Uri.parse(url)))
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.map_outlined, size: 80, color: Colors.teal),
            const SizedBox(height: 16),
            const Text('Map Viewer', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text('Loading: $url', style: const TextStyle(color: Colors.grey)),
            const SizedBox(height: 24),
            const Text('(Make sure backend is running!)'),
          ],
        ),
      ),
    );
  }
}
