struct BinaryHeap(T)
{
    T[] array = [T.init,];
	//invariant() { assert (array.length > 0); }
	void insert(ref T x)
	{
		array.length = array.length + 1;
		int index = array.length - 1;
		while (x < array[index / 2])
		{
			assert (index != 0);
			array[index] = array[index / 2];
			index /= 2;
		}
		array[index] = x;
	}
	T pop()
	{
		assert (array.length - 1 > 0);
		T ret = array[1];
		T last = array[1] = array[$ - 1];
		array.length = array.length - 1;
		if (array.length < 2) // no elements
			return ret;
		int node_index = 1;
		while (node_index * 2 < array.length)  // until there is atleast one child
		{
			int child_index = node_index * 2;
			if (child_index + 1 < array.length && array[child_index + 1] < array[child_index])
				child_index++;
			if (array[child_index] >= last)
				break;
			array[node_index] = array[child_index];
			node_index = child_index;
		}
		array[node_index] = last;
		return ret;
	}
	ref T get() { return this.array[1]; }
}

import std.date;
import std.conv;
import std.stdio;
alias d_time delegate(const ref d_time) Tasklet;

struct Task
{
	d_time time; Tasklet update;
	int opCmp(ref Task other)
	{
		return this.time > other.time ? 1 : this.time < other.time ? -1 : 0;
	}
}

import core.sync.condition;
import core.sync.mutex;
import core.thread;

const sleep_ticks = 10_000_000/ticksPerSecond;

void main()
{
	writeln("ticksPerSecond: ", ticksPerSecond);
	bool done = false;
	auto mutex = new Mutex;
	auto cond = new Condition(mutex);
	BinaryHeap!(Task) tasks;
	void task_mgr()
	{
		while (!done)
		{
			if (tasks.array.length < 2)  // no tasks
			{
				synchronized (mutex) cond.wait();
				continue;
			}

			auto now = getUTCtime();
			Task task = tasks.get();
			if (now < task.time)
			{
				synchronized (mutex) cond.wait((task.time - now) * sleep_ticks);
				if (getUTCtime() < task.time)
					writefln("### woke up too soon!");
				continue;
			}

			task = tasks.pop();
			auto timeout = task.update(now);
			if (timeout != d_time_nan)
			{
				task.time = now + timeout;
				tasks.insert(task);
			}
		}
	}
	auto worker = new Thread(&task_mgr);
	worker.start();
	   	char[] buf;
	int i;
	while (readln(buf))
	{
		if (buf[0] == ' ')
		{
			done = true;
			break;
		}
		auto timeout = 10*ticksPerSecond;//to!(int)(buf);
		tasks.insert(make_task(100*i++, timeout));
		cond.notify(); //synchronized?
	}
}

struct Time { int ms, sec, min, hour; }
ref Time format_time(ref d_time time)
{
	return Time(
			cast(int)(time%ticksPerSecond),
			cast(int)(time/ticksPerSecond%60),
			cast(int)(time/ticksPerSecond/60%60),
			cast(int)(time/ticksPerSecond/60/60%24));
}

ref Task make_task(int i, int timeout)
{
	writefln("adding a task with timeout(%s) ...", timeout);
	d_time next_time = getUTCtime() + timeout;
	int task_no = i;
	d_time task(const ref d_time time)
	{
		writefln("  <--  I am a task [%s] (diff: %s) {timeout: %s} -->", task_no++, next_time-time, timeout);
		next_time = time + timeout;
		return timeout;
	}
	return Task(next_time, &task);
}
