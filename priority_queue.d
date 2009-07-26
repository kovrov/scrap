import core.thread;
import core.sync.condition;
import core.sync.mutex;
import std.date;

const sleep_ticks = 10_000_000/ticksPerSecond;

class TaskQueue(T) : Thread
{
	this()
	{
		super(&run);
		this.mutex = new Mutex;
		this.cond = new Condition(this.mutex);
	}

	void enqueue(T x)
	{
		synchronized (this.mutex)
		{
			assert (!this.busy);
			this.insert(x);
			this.cond.notify();
		}
	}

	void stop()
	{
		synchronized (this.mutex)
		{
			this.done = true;
			this.cond.notify();
		}
	}

  private:
	bool busy;
	void run()
	{
		while (!this.done)
		{
			synchronized (this.mutex)
			{
				this.busy = true;
				scope (exit) this.busy = false;
				if (this.heap.length < 2)  // no tasks
				{
					cond.wait();
					debug writefln("+++ woke up to do something?");
					continue;
				}

				auto now = getUTCtime();
				auto task = this.heap[1];
				if (now < task.time)
				{
					cond.wait((task.time - now) * sleep_ticks);
					debug
					{	now = getUTCtime();
						if (now < task.time)
							debug writefln("### woke up too soon! (%s.%s sec earlier)",
									(task.time - now) / ticksPerSecond % 60,
									(task.time - now) % ticksPerSecond);
					}
					continue;
				}

				task = this.pop();
				auto timeout = task.update(now);
				if (timeout != d_time_nan)
				{
					task.time = now + timeout;
					this.insert(task);
				}
			}
		}
	}

	/* binary heap stuff */
	void insert(T x)
	{
		this.heap.length = this.heap.length + 1;
		int index = this.heap.length - 1;
		while (x < this.heap[index / 2])
		{
			assert (index != 0);
			this.heap[index] = this.heap[index / 2];
			index /= 2;
		}
		this.heap[index] = x;
	}
	T pop()
	{
		assert (this.heap.length - 1 > 0);
		T ret = this.heap[1];
		T last = this.heap[1] = this.heap[$ - 1];
		this.heap.length = this.heap.length - 1;
		if (this.heap.length < 2) // no elements
			return ret;
		int node_index = 1;
		while (node_index * 2 < this.heap.length)  // until there is atleast one child
		{
			int child_index = node_index * 2;
			if (child_index + 1 < this.heap.length && this.heap[child_index + 1] < this.heap[child_index])
				child_index++;
			if (this.heap[child_index] >= last)
				break;
			this.heap[node_index] = this.heap[child_index];
			node_index = child_index;
		}
		this.heap[node_index] = last;
		return ret;
	}

	bool done;
	Condition cond;
	Mutex mutex;
    T[] heap = [T.init,];
	//invariant() { assert (this.heap.length > 0); }
}

alias d_time delegate(const ref d_time) Tasklet;
struct Task
{
	d_time time; Tasklet update;
	int opCmp(ref Task other) { return this.time > other.time ? 1 : this.time < other.time ? -1 : 0; }
}

struct Time
{
	int hour, min, sec, ms;
	this(ref d_time time)
	{
		ms = cast(int)(time%ticksPerSecond);
		sec = cast(int)(time/ticksPerSecond%60);
		min = cast(int)(time/ticksPerSecond/60%60);
		hour = cast(int)(time/ticksPerSecond/60/60%24);
	}
}

Tasklet make_task(int i, int timeout)
{
	d_time next_time = getUTCtime() + timeout;
	int task_no = i;
	d_time task(const ref d_time time)
	{
		writefln("  <--  I am a task [%s] (diff: %s) {timeout: %s} -->", task_no++, next_time - time, timeout);
		next_time = time + timeout;
		return timeout;
	}
	return &task;
}
/+
d_time task_creator(const ref d_time time)
{
	writefln("  <--  I am a task '%s' (diff: %s) {timeout: %s} -->", "creator", next_time-time, timeout);
	next_time = time + timeout;
	d_time task(const ref d_time time)
	{
		writefln("  <--  I am a task [%s] (diff: %s) {timeout: %s} -->", task_no++, next_time-time, timeout);
		next_time = time + timeout;
		return timeout;
	}
	task_mgr.insert(make_task(100*i++, timeout));
	return timeout;
}
+/

import std.conv;
import std.stdio;

void main()
{
	auto task_mgr = new TaskQueue!(Task);
	//task_mgr.priority = Thread.PRIORITY_MAX; // test
	task_mgr.start();
	scope (exit) task_mgr.stop();

	char[] buf;
	int i;
	while (readln(buf))
	{
		try
		{
			auto timeout = to!(int)(buf[0..$-1]) * ticksPerSecond;;
			writefln("adding a task with timeout(%s) ...", timeout);
			task_mgr.enqueue(Task(timeout, make_task(100*i++, timeout)));
		}
		catch
		{
			break;
		}
	}
}

