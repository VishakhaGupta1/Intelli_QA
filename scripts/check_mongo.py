from pymongo import MongoClient

c = MongoClient('mongodb://127.0.0.1:27017')
db = c['qa_platform']
print('test_results:', db.test_results.count_documents({}))
print('defect_logs:', db.defect_logs.count_documents({}))
print('gap_reports:', db.gap_reports.count_documents({}))
