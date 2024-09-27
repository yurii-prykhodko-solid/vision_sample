from flask import Flask, request, jsonify

app = Flask(__name__)

supabase = init_supabase()
video_processing_queue = ProcessingQueue(supabase)

@app.route('/public/video', methods=['POST'])
def post_video():
    video_url = request.json.get('video_url')
    if not video_url:
        return jsonify({"error": "video_url is required"}), 400
	
    video_token = video_processing_queue.add(video_url)
		
    return jsonify({"token": video_token}) # best to generate a public-facing UUID instead of exposing int DB IDs.

@app.route('/public/video/status', methods=['GET'])
def get_video_status():
    video_token = request.json.get('token')
    if not video_token:
        return jsonify({"error": "token is required"}), 400
	
    status = video_processing_queue.get_video_processing_step(video_token)
    
    if not status:
        return jsonify('Not Found'), 404
		
    return jsonify({"status": status})


@app.route('/internal/perform-video-processing', methods=['POST'])
def perform_video_processing():
	video_id = video_processing_queue.pop() # marks it as in_progress

	try:
		process_video()
		video_processing_queue.mark_completed(video_id)
	except(e):
		video_processing_queue.mark_failed(video_id, e)
		if not is_fatal(e):
			video_processing_queue.mark_for_retry(video_id)

if __name__ == '__main__':
    app.run()
