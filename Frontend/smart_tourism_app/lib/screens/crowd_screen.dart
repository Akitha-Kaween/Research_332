
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import '../services/api_service.dart';

class CrowdAnalysisScreen extends StatefulWidget {
  const CrowdAnalysisScreen({super.key});

  @override
  State<CrowdAnalysisScreen> createState() => _CrowdAnalysisScreenState();
}

class _CrowdAnalysisScreenState extends State<CrowdAnalysisScreen> {
  String _selectedLocation = 'Kandy';
  DateTime _selectedDate = DateTime.now();
  bool _isLoading = false;
  Map<String, dynamic>? _result;

  final List<String> _locations = ['Colombo', 'Kandy', 'Galle', 'Sigiriya', 'Nuwara Eliya', 'Anuradhapura'];

  void _analyze() async {
    setState(() => _isLoading = true);
    final dateStr = DateFormat('yyyy-MM-dd').format(_selectedDate);
    final api = Provider.of<ApiService>(context, listen: false);
    final data = await api.getCrowdPrediction(_selectedLocation, dateStr);
    
    setState(() {
      _isLoading = false;
      _result = data;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Crowd Monitor')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            // Controls
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(12)),
              child: Column(
                children: [
                  DropdownButtonFormField(
                    value: _selectedLocation,
                    items: _locations.map((loc) => DropdownMenuItem(value: loc, child: Text(loc))).toList(),
                    onChanged: (val) => setState(() => _selectedLocation = val!),
                    decoration: const InputDecoration(labelText: 'Location', border: OutlineInputBorder()),
                  ),
                  const SizedBox(height: 16),
                  ListTile(
                    title: Text('Date: ${DateFormat('yyyy-MM-dd').format(_selectedDate)}'),
                    trailing: const Icon(Icons.calendar_today),
                    onTap: () async {
                      final picked = await showDatePicker(
                        context: context,
                        initialDate: _selectedDate,
                        firstDate: DateTime.now(),
                        lastDate: DateTime(2027),
                      );
                      if (picked != null) setState(() => _selectedDate = picked);
                    },
                    shape: RoundedRectangleBorder(side: BorderSide(color: Colors.grey.shade400), borderRadius: BorderRadius.circular(4)),
                  ),
                  const SizedBox(height: 16),
                  SizedBox(
                    width: double.infinity,
                    height: 50,
                    child: ElevatedButton(
                      onPressed: _isLoading ? null : _analyze,
                      style: ElevatedButton.styleFrom(backgroundColor: Colors.blueAccent, foregroundColor: Colors.white),
                      child: _isLoading ? const CircularProgressIndicator(color: Colors.white) : const Text('Analyze Crowd'),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),

            // Results
            if (_result != null)
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: Colors.blueAccent.withOpacity(0.3)),
                ),
                child: Column(
                  children: [
                    Text(
                      _result!['crowd_level'].toString().toUpperCase(),
                      style: TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                        color: _getColorForLevel(_result!['crowd_level']),
                      ),
                    ),
                    const Text('Predicted Crowd Level'),
                    const SizedBox(height: 24),
                    LinearProgressIndicator(
                      value: (_result!['crowd_percentage'] as int) / 100,
                      backgroundColor: Colors.grey.shade200,
                      color: _getColorForLevel(_result!['crowd_level']),
                      minHeight: 10,
                    ),
                    const SizedBox(height: 16),
                    Text('${_result!['expected_visitors']} Visitors Expected', style: const TextStyle(fontSize: 16)),
                  ],
                ),
              ),
          ],
        ),
      ),
    );
  }

  Color _getColorForLevel(String? level) {
    if (level == 'high') return Colors.red;
    if (level == 'medium') return Colors.orange;
    return Colors.green;
  }
}
