
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/api_service.dart';

class FoodRecommendationScreen extends StatefulWidget {
  const FoodRecommendationScreen({super.key});

  @override
  State<FoodRecommendationScreen> createState() => _FoodRecommendationScreenState();
}

class _FoodRecommendationScreenState extends State<FoodRecommendationScreen> {
  bool _isLoading = false;
  List<dynamic> _recommendations = [];

  void _getRecommendations() async {
    setState(() => _isLoading = true);
    final api = Provider.of<ApiService>(context, listen: false);
    // Hardcoded User ID 1 for demo
    final data = await api.getFoodRecommendations(1);
    
    setState(() {
      _isLoading = false;
      _recommendations = data;
    });
  }

  // Mock Data Helper since API only returns IDs
  String _getName(int id) => 'Spicy Sri Lankan Curry #$id';
  String _getImage(int id) => 'https://source.unsplash.com/200x200/?curry,food';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Foodie Finder')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                gradient: const LinearGradient(colors: [Colors.orangeAccent, Colors.deepOrange]),
                borderRadius: BorderRadius.circular(16),
              ),
              child: Row(
                children: [
                  const Expanded(
                    child: Text(
                      'Discover personalized flavors tailored to your taste!',
                      style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                  ),
                  const SizedBox(width: 8),
                  ElevatedButton(
                    onPressed: _isLoading ? null : _getRecommendations,
                    style: ElevatedButton.styleFrom(backgroundColor: Colors.white, foregroundColor: Colors.deepOrange),
                    child: _isLoading ? const Padding(padding: EdgeInsets.all(4), child: CircularProgressIndicator(strokeWidth: 2)) : const Text('Suggest'),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),

            // List
            const Text('Top Picks for You', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            
            Expanded(
              child: _recommendations.isEmpty
                  ? Center(child: Text(_isLoading ? 'Fetching...' : 'Tap Suggest to start!', style: TextStyle(color: Colors.grey)))
                  : ListView.builder(
                      itemCount: _recommendations.length,
                      itemBuilder: (context, index) {
                        final item = _recommendations[index];
                        return Card(
                          margin: const EdgeInsets.only(bottom: 16),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                          child: ListTile(
                            contentPadding: const EdgeInsets.all(12),
                            leading: ClipRRect(
                              borderRadius: BorderRadius.circular(8),
                              child: Container(color: Colors.grey.shade300, width: 60, height: 60, child: const Icon(Icons.fastfood, color: Colors.grey)),
                              // Use CachedNetworkImage in real app
                            ),
                            title: Text(_getName(item['recipe_id'])),
                             subtitle: Row(
                               children: [
                                 const Icon(Icons.star, size: 16, color: Colors.amber),
                                 Text(' ${item['predicted_rating']} / 5.0'),
                               ],
                             ),
                            trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                          ),
                        );
                      },
                    ),
            ),
          ],
        ),
      ),
    );
  }
}
