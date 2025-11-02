import hashlib
import bcrypt
from app.models import db, CrackingJob, UserStatistics
from datetime import datetime
import os

DEFAULT_WORDLIST = os.path.join(os.path.dirname(__file__), '..', '..', 'wordlists', 'common.txt')

def submit_cracking_job(job_id):
    """Submit a cracking job to be processed"""
    # In a production environment, this would submit to Celery
    # For now, we'll process synchronously for demonstration
    try:
        from threading import Thread
        thread = Thread(target=process_job, args=(job_id,))
        thread.daemon = True
        thread.start()
    except Exception as e:
        print(f"Error submitting job: {e}")


def process_job(job_id):
    """Process a cracking job"""
    job = CrackingJob.query.get(job_id)
    
    if not job:
        return
    
    try:
        # Update job status
        job.status = 'processing'
        job.started_at = datetime.utcnow()
        db.session.commit()
        
        # Get wordlist path
        wordlist_path = DEFAULT_WORDLIST
        
        # Check if wordlist exists, if not use a small default list
        if not os.path.exists(wordlist_path):
            # Create a minimal wordlist for testing
            wordlist = ['password', 'password123', '123456', 'admin', 'test', 'qwerty']
        else:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                wordlist = [line.strip() for line in f if line.strip()]
        
        # Crack the hash
        result = crack_hash(
            job.hash_value,
            job.hash_type,
            wordlist
        )
        
        if result:
            job.status = 'completed'
            job.result = result['password']
            job.attempts = result['attempts']
            
            # Update user statistics
            user_stats = UserStatistics.query.filter_by(user_id=job.user_id).first()
            if user_stats:
                user_stats.successful_cracks += 1
                user_stats.total_hashes_cracked += 1
                user_stats.total_attempts += result['attempts']
        else:
            job.status = 'failed'
            job.attempts = len(wordlist)
            
            # Update user statistics
            user_stats = UserStatistics.query.filter_by(user_id=job.user_id).first()
            if user_stats:
                user_stats.failed_attempts += 1
                user_stats.total_attempts += len(wordlist)
        
        job.completed_at = datetime.utcnow()
        db.session.commit()
        
    except Exception as e:
        print(f"Error processing job {job_id}: {e}")
        job.status = 'failed'
        job.completed_at = datetime.utcnow()
        db.session.commit()


def crack_hash(hash_value, hash_type, wordlist):
    """Attempt to crack a hash using a wordlist"""
    attempts = 0
    
    for password in wordlist:
        attempts += 1
        
        try:
            if check_hash(password, hash_value, hash_type):
                return {
                    'password': password,
                    'attempts': attempts
                }
        except Exception as e:
            print(f"Error checking password: {e}")
            continue
    
    return None


def check_hash(password, hash_value, hash_type):
    """Check if a password matches a hash"""
    password_bytes = password.encode('utf-8')
    
    if hash_type == 'bcrypt':
        # Normalize bcrypt hash
        normalized_hash = hash_value.replace('$2y$', '$2b$').encode('utf-8')
        try:
            return bcrypt.checkpw(password_bytes, normalized_hash)
        except Exception:
            return False
    
    elif hash_type == 'md5':
        return hashlib.md5(password_bytes).hexdigest() == hash_value
    
    elif hash_type == 'sha1':
        return hashlib.sha1(password_bytes).hexdigest() == hash_value
    
    elif hash_type == 'sha256':
        return hashlib.sha256(password_bytes).hexdigest() == hash_value
    
    return False


def detect_hash_type(hash_value):
    """Detect the type of hash"""
    if hash_value.startswith('$2y$') or hash_value.startswith('$2b$'):
        return 'bcrypt'
    elif len(hash_value) == 32:
        return 'md5'
    elif len(hash_value) == 40:
        return 'sha1'
    elif len(hash_value) == 64:
        return 'sha256'
    else:
        return 'unknown'
